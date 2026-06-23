(function ($) {
    DjangoMapWidgetPolygonBase = $.Class.extend({

        init: function (options) {
            $.extend(this, options);
            this.coordinatesOverlayToggleBtn.on("click", this.toggleCoordinatesOverlay.bind(this));
            this.coordinatesOverlayDoneBtn.on("click", this.handleCoordinatesOverlayDoneBtnClick.bind(this));
            this.wktOverlayInput.on("change", this.handleWktInputChange.bind(this));
            if (this.coordinatesOverlayCopyBtn && this.coordinatesOverlayCopyBtn.length) {
                this.coordinatesOverlayCopyBtn.on("click", this.handleCopyClick.bind(this));
            }
            this.drawPolygonBtn.on("click", this.handleDrawBtnClick.bind(this));
            this.myLocationBtn.on("click", this.handleMyLocationBtnClick.bind(this));
            this.deleteBtn.on("click", this.resetMap.bind(this));

            // if the field is in a collapsed Django admin fieldset, the map needs to
            // initialize again when the collapse is opened by the user.
            if ($(this.wrapElemSelector).closest('.module.collapse').length) {
                $(document).on('show.fieldset', this.initializeMap.bind(this));
            }
            this.initializeMap.bind(this)();
            this.djangoInput.data('mwMapObj', this.map);
            this.djangoInput.data('mwClassObj', this);
        },

        // --- Methods to implement per map JS library ---------------------------------

        initializeMap: function () {
            console.warn("Implement initializeMap method.");
        },

        enterDrawMode: function () {
            console.warn("Implement enterDrawMode method.");
        },

        exitDrawMode: function () {
            console.warn("Implement exitDrawMode method.");
        },

        finishPolygon: function () {
            console.warn("Implement finishPolygon method.");
        },

        loadPolygon: function (geojson) {
            console.warn("Implement loadPolygon method.");
        },

        removePolygon: function () {
            console.warn("Implement removePolygon method.");
        },

        fitBoundsPolygon: function () {
            console.warn("Implement fitBoundsPolygon method.");
        },

        serializePolygonToGeoJSON: function () {
            console.warn("Implement serializePolygonToGeoJSON method.");
        },

        panToLocation: function (lat, lng) {
            console.warn("Implement panToLocation method.");
        },

        // --- Shared behaviour --------------------------------------------------------

        isDrawing: false,

        enableClearBtn: function () {
            this.deleteBtn.removeClass("mw-btn-default disabled").addClass("mw-btn-danger");
        },

        disableClearBtn: function () {
            this.deleteBtn.removeClass("mw-btn-danger").addClass("mw-btn-default disabled");
        },

        updateDjangoInput: function () {
            const geojson = this.serializePolygonToGeoJSON();
            if (!geojson) {
                return;
            }
            this.djangoInput.val(JSON.stringify(geojson));
            this.wktOverlayInput.val(this.polygonGeoJSONToWKT(geojson));
            this.djangoGeoJSONValue = {geojson: geojson};
            this.enableClearBtn();
        },

        resetMap: function () {
            if ($.isEmptyObject(this.djangoGeoJSONValue)) {
                return;
            }
            this.exitDrawMode();
            this.hideOverlay();
            this.removePolygon();
            this.djangoInput.val("");
            this.wktOverlayInput.val("");
            this.disableClearBtn();
            $(document).trigger(this.polygonDeleteTriggerNameSpace,
                [this.djangoGeoJSONValue, this.wrapElemSelector, this.djangoInput]);
            this.djangoGeoJSONValue = null;
        },

        handleDrawBtnClick: function () {
            if (this.isDrawing) {
                this.exitDrawMode();
            } else {
                this.enterDrawMode();
            }
        },

        toggleCoordinatesOverlay: function () {
            this.coordinatesOverlayToggleBtn.toggleClass("active");
            $(".mw-coordinates-overlay", this.wrapElemSelector).toggleClass("hide");
        },

        handleCoordinatesOverlayDoneBtnClick: function () {
            $(".mw-coordinates-overlay", this.wrapElemSelector).addClass("hide");
            this.coordinatesOverlayToggleBtn.removeClass("active");
        },

        handleCopyClick: function () {
            const text = this.wktOverlayInput.val() || "";
            if (!text) {
                return;
            }
            const label = $(".button-text", this.coordinatesOverlayCopyBtn);
            const original = label.text();
            const showCopied = function () {
                label.text("Copied!");
                setTimeout(function () {
                    label.text(original);
                }, 1500);
            };
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(text).then(showCopied, this.fallbackCopy.bind(this, text, showCopied));
            } else {
                this.fallbackCopy(text, showCopied);
            }
        },

        fallbackCopy: function (text, onDone) {
            const textarea = this.wktOverlayInput.get(0);
            if (textarea) {
                textarea.focus();
                textarea.select();
                try {
                    document.execCommand("copy");
                } catch (e) {
                    // clipboard not available
                }
            }
            if (onDone) {
                onDone();
            }
        },

        handleWktInputChange: function () {
            const text = (this.wktOverlayInput.val() || "").trim();
            if (!text) {
                return;
            }
            const geojson = this.wktToGeoJSON(text);
            if (!geojson) {
                alert("Could not parse the geometry. Provide a valid WKT polygon, e.g. POLYGON((lng lat, ...)).");
                return;
            }
            this.removePolygon();
            this.loadPolygon(geojson);
            this.updateDjangoInput();
            this.fitBoundsPolygon();
        },

        // --- Geometry text helpers (provider agnostic) -------------------------------

        // Build "POLYGON((lng lat, lng lat, ...))" from a GeoJSON Polygon (outer ring).
        polygonGeoJSONToWKT: function (geojson) {
            const ring = geojson.coordinates[0] || [];
            const pairs = ring.map(function (c) {
                return c[0] + " " + c[1];
            });
            return "POLYGON((" + pairs.join(", ") + "))";
        },

        // Parse a single-ring "POLYGON((lng lat, ...))" string into a GeoJSON Polygon.
        wktToGeoJSON: function (wkt) {
            const match = /POLYGON\s*\(\(\s*(.+?)\s*\)\)/i.exec(wkt);
            if (!match) {
                return null;
            }
            const coords = match[1].split(",").map(function (pair) {
                const xy = pair.trim().split(/\s+/);
                return [parseFloat(xy[0]), parseFloat(xy[1])];
            });
            if (coords.length < 3 || coords.some(function (c) {
                return isNaN(c[0]) || isNaN(c[1]);
            })) {
                return null;
            }
            return {type: "Polygon", coordinates: [coords]};
        },

        // --- Geolocation -------------------------------------------------------------

        handleMyLocationBtnClick: function () {
            this.showOverlay();
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    this.handleCurrentPosition.bind(this),
                    this.handlecurrentPositionError.bind(this)
                );
            } else {
                this.handlecurrentPositionError();
            }
        },

        handleCurrentPosition: function (location) {
            this.panToLocation(location.coords.latitude, location.coords.longitude);
            this.hideOverlay();
        },

        handlecurrentPositionError: function () {
            this.hideOverlay();
            alert("Your location could not be found.");
        },

        showOverlay: function () {
            this.loaderOverlayElem.removeClass("hide");
        },

        hideOverlay: function () {
            this.loaderOverlayElem.addClass("hide");
        }
    });

})(mapWidgets.jQuery);
