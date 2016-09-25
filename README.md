### Django Map Widgets
Configurable, pluggable and more user friendly map widgets for Django PostGIS fields.

### Achievements
The aim of the Django map widgets is to make all Geo Django widgets more user friendly and configurable. Map widgets support major map services (GoogleMaps, OpenStreetMap) for your geoDjango fields.

### Installation

    pip install django-map-widgets

    
Add ‘map_widgets’ to your `INSTALLED_APPS` in settings.py

```python
INSTALLED_APPS = [
     ...
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'mapwidgets',
]
```

### Requirements

Django map widgets requires jQuery framework, it does not import jQuery library. It's working with your global jQuery. If you will use map widgets in Django Admin, you don't need to add jQuery. Map widgets work with Django Admin jQuery file. 

### PointField Map Widgets

#### Google Map Widget
##### Settings

* **GOOGLE_MAP_API_KEY**: Put your Google API key

* **mapCenterLocationName**: You can give a specific location name for center of map. Map widget will find this location coordinates using <a href="https://developers.google.com/maps/documentation/javascript/examples/places-autocomplete" target="_blank">Google Places Autocomplete</a>. (Optional)

* **mapCenterLocation**: You can give specific coordinates for center of the map. Coordinates must be list type. ([latitude, longitude]) (Optional)

* **zoom** : Default zoom value.

> Note: If there is no spesific value set for the map center, (mapCenterLocationName, mapCenterLocation) the widget will be centered by the timezone setting of the project.

Check out these links.

- <a href="https://github.com/erdem/django-map-widgets/blob/master/mapwidgets/constants.py">Timezone Center Locations</a>
- <a href="https://gist.github.com/erdem/8c7d26765831d0f9a8c62f02782ae00d">countries.json</a>


### Usage 

**settings.py**    
```python
MAP_WIDGETS = {
    "GooglePointFieldWidget": (
        ("zoom", 15),
        ("mapCenterLocationName", "london"),
    ),
    "GOOGLE_MAP_API_KEY": "<google-map-api-key>"
}
```

If you want to give specific coordinates for center of the map, you can update your settings file like that. 

```python
MAP_WIDGETS = {
    "GooglePointFieldWidget": (
        ("zoom", 15),
        ("mapCenterLocation", [57.7177013, -16.6300491]),
    ),
    "GOOGLE_MAP_API_KEY": "<google-map-api-key>"
}
```

#### Django Admin
```python
from mapwidgets.widgets import GooglePointFieldWidget

class CityAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }
```

#### Django Forms
```python
from mapwidgets.widgets import GooglePointFieldWidget

class CityAdminForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ("coordinates", "city_hall")
        widgets = {
            'coordinates': GooglePointFieldWidget,
            'city_hall': GooglePointFieldWidget,
        }
```
#### Preview

![](https://cloud.githubusercontent.com/assets/1518272/18732352/724dd098-805a-11e6-8eb4-6ba9b5e06a81.png)

#### jQuery Triggers

If you want develop your map UI on front-end side, you can use map widget jQuery triggers.  

* **google_point_map_widget:marker_create**: Triggered when user create first marker on map. *callback params: lat, lng, locationInputElem, mapWrapID*

* **google_point_map_widget:marker_change**: Triggered when user change marker position on map. *callback params: lat, lng, locationInputElem, mapWrapID*

* **google_point_map_widget:marker_delete**: Triggered when user delete marker on map. *callback params: lat, lng, locationInputElem, mapWrapID*
        

```javascript
$(document).on("google_point_map_widget:marker_create", function (e, lat, lng, locationInputElem, mapWrapID) {
    console.log(locationInputElem); // django widget textarea widget (hidden)
    console.log(lat, lng); // created marker coordinates
    console.log(mapWrapID); // map widget wrapper element ID
});

$(document).on("google_point_map_widget:marker_change", function (e, lat, lng, locationInputElem, mapWrapID) {
    console.log(locationInputElem); // django widget textarea widget (hidden)
    console.log(lat, lng);  // changed marker coordinates
    console.log(mapWrapID); // map widget wrapper element ID
});

$(document).on("google_point_map_widget:marker_delete", function (e, lat, lng, locationInputElem, mapWrapID) {
    console.log(locationInputElem); // django widget textarea widget (hidden)
    console.log(lat, lng);  // deleted marker coordinates
    console.log(mapWrapID); // map widget wrapper element ID
})
```


#### Google Map Widget for Django Admin Inlines

As you know Django Admin has inline feature and you can add an inline row dynamically. In this case, Django default map widget doesn't initialize widget when created a new inline row. 

If you want to use Google Map Widget on admin inlines with no issue, you just need to use `GooglePointFieldInlineWidget` class. 

#### Example
```python
from mapwidgets.widgets import GooglePointFieldInlineWidget

class DistrictAdminInline(admin.TabularInline):
    model = District
    extra = 3
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldInlineWidget}
    }
    
class CityAdmin(admin.ModelAdmin):
    inlines = (DistrictAdminInline,)
```

#### Preview
![](https://cloud.githubusercontent.com/assets/1518272/18221609/2cac10fe-7178-11e6-9990-a93176693ef7.gif)
### Google Static Map Widget (ReadOnly)

#### Settings

Django map widgets provide all Google Static Map API features. Check out this <a href="https://developers.google.com/maps/documentation/static-maps/intro" target="_blank">link</a> for google static map api features. 

Here is the all default settings attribute for google static map widget.

```python
MAP_WIDGETS = {
    "GoogleStaticMapWidget": (
        ("zoom", 15),
        ("size", "480x480"),
        ("scale", ""),
        ("format", ""),
        ("maptype", ""),
        ("path", ""),
        ("visible", ""),
        ("style", ""),
        ("language", ""),
        ("region", "")
    ),

    "GoogleStaticMapMarkerSettings": (
        ("size", "normal"),
        ("color", ""),
        ("icon", ""),
    )
    "GOOGLE_MAP_API_SIGNATURE": "",
    "GOOGLE_MAP_API_KEY": "",
}    
```

##### Usage

If you are not using specific features on Google Static Map API, you just need to update `GOOGLE_MAP_API_KEY` value in your Django settings file. If you need also individual size map images, you can pass `size` and `zoom` parameter for each `GoogleStaticMapWidget` class. 


#### Example

**settings.py**
```python
MAP_WIDGETS = {
    "GoogleStaticMapWidget": (
        ("zoom", 15),
        ("size", "320x320"),
    ),
    "GoogleStaticMapMarkerSettings": (
        ("color", "green"),
    )
    "GOOGLE_MAP_API_KEY": "<google-map-api-key>"
}
```

**forms.py**
```python
from mapwidgets.widgets import GoogleStaticMapWidget

class CityDetailForm(forms.ModelForm):

    class Meta:
        model = City
        fields = ("name", "coordinates", "city_hall")
        widgets = {
            'coordinates': GoogleStaticMapWidget,
            'city_hall': GoogleStaticMapWidget(zoom=12, size="240x240"),
        }
```

### Google Static Map Overlay Widget (ReadOnly)
This widget is working with <a href="https://developers.google.com/maps/documentation/static-maps/intro" target="_blank">Magnific Popup</a> jQuery plugin. 

##### Usage

You can use also all static map features in this widget. Besides you can give a `thumbnail_size` value. 
 
Here is the all default settings attribute for google static overlay map widget.

```python
MAP_WIDGETS = {
    "GoogleStaticMapMarkerSettings": (
        ("size", "normal"),
        ("color", ""),
        ("icon", ""),
    ),

    "GoogleStaticOverlayMapWidget": (
        ("zoom", 15),
        ("size", "480x480"),
        ("thumbnail_size", "160x160"),
        ("scale", ""),
        ("format", ""),
        ("maptype", ""),
        ("path", ""),
        ("visible", ""),
        ("style", ""),
        ("language", ""),
        ("region", "")
    ),

    "GOOGLE_MAP_API_SIGNATURE": "",
    "GOOGLE_MAP_API_KEY": "",
}   
```

#### Example

```python
from mapwidgets.widgets import GoogleStaticOverlayMapWidget


class CityDetailForm(forms.ModelForm):

    class Meta:
        model = City
        fields = ("name", "coordinates", "city_hall")
        widgets = {
            'coordinates': GoogleStaticOverlayMapWidget,
            'city_hall': GoogleStaticOverlayMapWidget(zoom=12, size="640x640", thumbnail_size="50x50"),
        }
```

#### Preview
![](https://cloud.githubusercontent.com/assets/1518272/18732296/18f1813e-805a-11e6-8801-f1f48ed02a9c.png)
