var mapWidgets = mapWidgets || {};
if (typeof django !== "undefined" && django.jQuery){
    mapWidgets.jQuery = django.jQuery.noConflict();
}else{
    mapWidgets.jQuery = jQuery.noConflict();
}


(function($) {

    var initializing = false, fnTest = /xyz/.test(function(){xyz;}) ? /\bSuper\b/ : /.*/;

    $.Class = function() {

    };

    $.Class.extend = function(prop) {
        var Super = this.prototype;

        initializing = true;
        var prototype = new this();
        initializing = false;

        for (var name in prop) {
            prototype[name] = typeof prop[name] == "function" && typeof Super[name] == "function" && fnTest.test(prop[name]) ? (function(name, fn) {
                return function() {
                    var tmp = this.Super;

                    this.Super = Super[name];

                    var ret = fn.apply(this, arguments);
                    this.Super = tmp;

                    return ret;
                };
            })(name, prop[name]) : prop[name];
        }

        function Class() {
            if (!initializing && this.init) {
                this.init.apply(this, arguments);
            }
        }

        Class.prototype = prototype;

        Class.constructor = Class;

        Class.extend = arguments.callee;

        return Class;
    };

    if (typeof Function.bind === 'undefined') {

        Function.prototype.bind = function(obj) {
            var method = this;

            tmp = function() {
                return method.apply(obj, arguments);
            };

            return tmp;
        };

    }

    if (!Array.indexOf){
        Array.prototype.indexOf = function(obj) {
            for (var i = 0; i < this.length; i++) {
                if (this[i] == obj) {
                    return i;
                }
            }

            return -1;
        };
    }

})(mapWidgets.jQuery);