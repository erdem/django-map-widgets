(function ($) {
    DjangoLeafletPolygonFieldWidget = DjangoMapWidgetPolygonBase.extend({

        initializeMap: function () {
            this.leafletMapOptions = this.mapOptions.mapOptions || {};
            if (!this.leafletMapOptions.center) {
                this.leafletMapOptions.center = this.mapCenterLocation;
            }
            this.leafletTileLayer = this.mapOptions.tileLayer;
            this.polygonStyle = this.mapOptions.polygonOptions || {};
            this.map = L.map(this.mapElement.id, this.leafletMapOptions);
            L.tileLayer(this.leafletTileLayer.urlTemplate, this.leafletTileLayer.options).addTo(this.map);
            if (this.map.zoomControl) {
                this.map.zoomControl.setPosition('topright');
            }
            $(this.mapElement).data("mwMapObj", this.map);
            $(this.mapElement).data("mwClassObj", this);

            this.polygon = null;
            this.vertexMarkers = [];
            this.drawLatLngs = [];
            this.drawVertexMarkers = [];
            this.drawPreview = null;

            if (!$.isEmptyObject(this.djangoGeoJSONValue) && this.djangoGeoJSONValue.geojson) {
                this.loadPolygon(this.djangoGeoJSONValue.geojson);
                this.updateDjangoInput();
                if (this.mapOptions.fitBoundsOnLoad !== false) {
                    this.fitBoundsPolygon();
                }
            }
        },

        // --- Drawing -----------------------------------------------------------------

        enterDrawMode: function () {
            this.removePolygon();
            this.isDrawing = true;
            this.drawPolygonBtn.addClass("active");
            $(this.mapElement).addClass("click");
            this.drawLatLngs = [];
            this.drawVertexMarkers = [];
            this.drawPreview = null;
            this.map.doubleClickZoom.disable();
            this.map.on("click", this.handleMapClick, this);
            this.map.on("dblclick", this.finishPolygon, this);
        },

        exitDrawMode: function () {
            if (!this.isDrawing) {
                return;
            }
            this.isDrawing = false;
            this.drawPolygonBtn.removeClass("active");
            $(this.mapElement).removeClass("click");
            this.map.off("click", this.handleMapClick, this);
            this.map.off("dblclick", this.finishPolygon, this);
            this.map.doubleClickZoom.enable();
            this.clearDrawLayers();
        },

        clearDrawLayers: function () {
            const self = this;
            this.drawVertexMarkers.forEach(function (m) {
                self.map.removeLayer(m);
            });
            this.drawVertexMarkers = [];
            if (this.drawPreview) {
                this.map.removeLayer(this.drawPreview);
                this.drawPreview = null;
            }
            this.drawLatLngs = [];
        },

        // pixel radius around the first vertex that closes the ring
        CLOSE_TOLERANCE: 12,

        handleMapClick: function (e) {
            // Close the ring when the user clicks on/near the first vertex.
            if (this.drawLatLngs.length >= 3 && this.isNearFirstVertex(e.latlng)) {
                this.finishPolygon();
                return;
            }
            this.drawLatLngs.push(e.latlng);
            const isFirst = this.drawLatLngs.length === 1;
            const color = this.polygonStyle.color || "#3388ff";
            // non-interactive so clicks (even directly on the dot) reach the map and
            // get handled by the proximity check above, keeping the crosshair cursor.
            const vertex = L.circleMarker(e.latlng, {
                radius: isFirst ? 7 : 5,
                color: color,
                fillColor: isFirst ? color : "#ffffff",
                fillOpacity: 1,
                weight: 2,
                interactive: false
            }).addTo(this.map);
            this.drawVertexMarkers.push(vertex);
            this.updateDrawPreview();
        },

        isNearFirstVertex: function (latlng) {
            const firstPt = this.map.latLngToContainerPoint(this.drawLatLngs[0]);
            const clickPt = this.map.latLngToContainerPoint(latlng);
            return firstPt.distanceTo(clickPt) <= this.CLOSE_TOLERANCE;
        },

        dedupeLatLngs: function (latlngs) {
            const self = this;
            return latlngs.filter(function (latlng, i) {
                if (i === 0) {
                    return true;
                }
                const prev = self.map.latLngToContainerPoint(latlngs[i - 1]);
                const curr = self.map.latLngToContainerPoint(latlng);
                return prev.distanceTo(curr) > 1;
            });
        },

        updateDrawPreview: function () {
            if (this.drawPreview) {
                this.map.removeLayer(this.drawPreview);
            }
            this.drawPreview = L.polyline(this.drawLatLngs, {
                color: this.polygonStyle.color || "#3388ff",
                weight: this.polygonStyle.weight || 3,
                dashArray: "5,5",
                interactive: false
            }).addTo(this.map);
        },

        finishPolygon: function () {
            if (!this.isDrawing) {
                return;
            }
            // drop consecutive duplicate points (e.g. the extra click from a double-click)
            const latlngs = this.dedupeLatLngs(this.drawLatLngs);
            if (latlngs.length < 3) {
                return;
            }
            this.exitDrawMode();
            this.createEditablePolygon(latlngs);
            this.updateDjangoInput();
            // no re-fit here: the user just drew it, so it's already in view
            $(document).trigger(this.polygonCreateTriggerNameSpace,
                [this.serializePolygonToGeoJSON(), this.wrapElemSelector, this.djangoInput]);
        },

        // --- Editable polygon --------------------------------------------------------

        createEditablePolygon: function (latlngs) {
            this.polygon = L.polygon(latlngs, this.polygonStyle).addTo(this.map);
            this.buildVertexMarkers(latlngs);
        },

        buildVertexMarkers: function (latlngs) {
            const self = this;
            this.vertexMarkers = latlngs.map(function (latlng, index) {
                const marker = L.marker(latlng, {
                    draggable: true,
                    icon: L.divIcon({
                        className: "mw-vertex-handle",
                        iconSize: [12, 12]
                    })
                }).addTo(self.map);
                marker.on("drag", function () {
                    self.syncPolygonFromVertices();
                });
                marker.on("dragend", function () {
                    self.syncPolygonFromVertices();
                    self.updateDjangoInput();
                    $(document).trigger(self.polygonChangeTriggerNameSpace,
                        [self.serializePolygonToGeoJSON(), self.wrapElemSelector, self.djangoInput]);
                });
                return marker;
            });
        },

        syncPolygonFromVertices: function () {
            if (!this.polygon) {
                return;
            }
            const latlngs = this.vertexMarkers.map(function (m) {
                return m.getLatLng();
            });
            this.polygon.setLatLngs(latlngs);
        },

        loadPolygon: function (geojson) {
            const ring = (geojson.coordinates[0] || []).slice();
            // GeoJSON rings are closed (last == first); drop the closing point for editing.
            if (ring.length > 1) {
                const first = ring[0];
                const last = ring[ring.length - 1];
                if (first[0] === last[0] && first[1] === last[1]) {
                    ring.pop();
                }
            }
            const latlngs = ring.map(function (c) {
                return L.latLng(c[1], c[0]);
            });
            this.createEditablePolygon(latlngs);
        },

        removePolygon: function () {
            const self = this;
            if (this.polygon) {
                this.map.removeLayer(this.polygon);
                this.polygon = null;
            }
            (this.vertexMarkers || []).forEach(function (m) {
                self.map.removeLayer(m);
            });
            this.vertexMarkers = [];
            this.clearDrawLayers();
        },

        fitBoundsPolygon: function () {
            if (this.polygon) {
                this.map.fitBounds(this.polygon.getBounds(), {
                    maxZoom: this.mapOptions.polygonFitZoom || 14
                });
            }
        },

        panToLocation: function (lat, lng) {
            this.map.setView([lat, lng], this.mapOptions.polygonFitZoom || 14);
        },

        serializePolygonToGeoJSON: function () {
            if (!this.polygon) {
                return null;
            }
            const ring = this.polygon.getLatLngs()[0].map(function (latlng) {
                return [latlng.lng, latlng.lat];
            });
            if (ring.length < 3) {
                return null;
            }
            // close the ring as required by GeoJSON
            const first = ring[0];
            const last = ring[ring.length - 1];
            if (first[0] !== last[0] || first[1] !== last[1]) {
                ring.push([first[0], first[1]]);
            }
            return {type: "Polygon", coordinates: [ring]};
        }
    });

})(mapWidgets.jQuery);
