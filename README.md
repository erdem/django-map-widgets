### Django Map Widgets (Beta)
Pluggable map widgets for Django Postgis fields.

### Achievement


### Settings

* **GOOGLE_MAP_API_KEY**: Put your Google API key

* **mapCenterLocationName**: You can give specific location name for center of map. Map widget will found this location coordinates using <a href="https://developers.google.com/maps/documentation/javascript/examples/places-autocomplete" target="_blank"> Google Places Autocomplete</a>. (Optional)

* **mapCenterLocation**: You can give specific coordinates for center of map. Coordinates must be list type. ([latitude, longitude]) (Optional)

* **zoom** : Default zoom value.

Note: If there is no setted value for the map center, (mapCenterLocationName, mapCenterLocation) the widget will be centered by the timezone setting of project.

Check out this links.

- <a href="https://github.com/erdem/django-map-widgets/blob/master/mapwidgets/constants.py">Timezone Center Locations</a>
- <a href="https://gist.github.com/erdem/8c7d26765831d0f9a8c62f02782ae00d">countries.json</a>



**settings.py**    

    MAP_WIDGETS = {
        "mapCenterLocation": [57.7177013, -16.6300491],
        "zoom": 12,
        "GOOGLE_MAP_API_KEY": "AIzaSyDRIvN9brpxIm_xx129R9a_VTCcTN2bE"
    }




### Usage 

##### Django Admin
    
    from mapwidgets.widgets import GoogleMapWidget
    
    class CityAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": GoogleMapWidget}
    }


##### Django Forms

    from mapwidgets.widgets import GoogleMapWidget
    
    class CityAdminForm(forms.ModelForm):
        class Meta:
            model = City
            fields = ("coordinates", "city_hall")
            widgets = {
                'coordinates': GoogleMapWidget,
                'city_hall': GoogleMapWidget,
            }





## Screenshot

![](http://i.imgur.com/QpBycQu.png)
