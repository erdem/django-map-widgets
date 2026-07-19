(function ($) {
    // A small autocomplete search bar wired to a leaflet-geosearch provider.
    // It renders results into a custom dropdown (project styled) and calls
    // `onSelect(result)` with a leaflet-geosearch result object:
    //   { x: lng, y: lat, label, bounds: [[s, w], [n, e]], raw }
    DjangoMapWidgetGeoSearch = $.Class.extend({

        minQueryLength: 3,
        debounceWait: 300,

        init: function (options) {
            $.extend(this, options);
            this.results = [];
            this.activeIndex = -1;
            this.provider = this.buildProvider();
            if (!this.provider) {
                return;
            }
            this.input.attr("autocomplete", "off");
            this.input.on("input", this.debounce(this.handleInput.bind(this), this.debounceWait));
            this.input.on("keydown", this.handleKeydown.bind(this));
            $(document).on("click", this.handleDocumentClick.bind(this));
        },

        buildProvider: function () {
            const lib = window.GeoSearch;
            if (!lib) {
                console.warn("leaflet-geosearch (window.GeoSearch) is not loaded.");
                return null;
            }
            const Provider = lib[this.providerName] || lib.OpenStreetMapProvider;
            return new Provider(this.providerOptions || {});
        },

        handleInput: function () {
            const self = this;
            const query = $.trim(this.input.val());
            if (query.length < this.minQueryLength) {
                this.clearResults();
                return;
            }
            this.provider.search({query: query}).then(function (results) {
                self.renderResults(results || []);
            }).catch(function () {
                self.clearResults();
            });
        },

        renderResults: function (results) {
            this.results = results;
            this.activeIndex = -1;
            this.resultsContainer.empty();
            if (!results.length) {
                this.clearResults();
                return;
            }
            const self = this;
            results.forEach(function (result, index) {
                $("<li>")
                    .addClass("mw-geosearch-result-item")
                    .text(result.label)
                    .on("click", function () {
                        self.selectResult(index);
                    })
                    .appendTo(self.resultsContainer);
            });
            this.resultsContainer.removeClass("hide");
        },

        selectResult: function (index) {
            const result = this.results[index];
            if (!result) {
                return;
            }
            this.input.val(result.label);
            this.clearResults();
            if (typeof this.onSelect === "function") {
                this.onSelect(result);
            }
        },

        handleKeydown: function (e) {
            if (this.resultsContainer.hasClass("hide")) {
                return;
            }
            const items = $(".mw-geosearch-result-item", this.resultsContainer);
            if (e.key === "ArrowDown") {
                e.preventDefault();
                this.activeIndex = Math.min(this.activeIndex + 1, items.length - 1);
            } else if (e.key === "ArrowUp") {
                e.preventDefault();
                this.activeIndex = Math.max(this.activeIndex - 1, 0);
            } else if (e.key === "Enter") {
                e.preventDefault();
                if (this.activeIndex >= 0) {
                    this.selectResult(this.activeIndex);
                }
                return;
            } else if (e.key === "Escape") {
                this.clearResults();
                return;
            } else {
                return;
            }
            items.removeClass("active").eq(this.activeIndex).addClass("active");
        },

        handleDocumentClick: function (e) {
            if (!$(e.target).closest(this.resultsContainer).length &&
                !$(e.target).is(this.input)) {
                this.clearResults();
            }
        },

        clearResults: function () {
            this.results = [];
            this.activeIndex = -1;
            this.resultsContainer.empty().addClass("hide");
        },

        debounce: function (fn, wait) {
            let timeout;
            return function () {
                const ctx = this, args = arguments;
                clearTimeout(timeout);
                timeout = setTimeout(function () {
                    fn.apply(ctx, args);
                }, wait);
            };
        }
    });

})(mapWidgets.jQuery);
