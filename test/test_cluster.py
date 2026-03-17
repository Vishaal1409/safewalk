import folium
from folium.plugins import MarkerCluster
try:
    from folium.utilities import JsCode
except ImportError:
    try:
        from branca.utilities import JsCode
    except ImportError:
        class JsCode:
            pass

m = folium.Map(location=[13.0827, 80.2707], zoom_start=12)
options = {
    "maxClusterRadius": folium.utilities.JsCode("""
    function(zoom) {
        return (500 * Math.pow(2, zoom)) / (156543.03392 * Math.cos(13.0827 * Math.PI / 180));
    }
    """) if hasattr(folium, 'utilities') and hasattr(folium.utilities, 'JsCode') else "TEST"
}
mc = MarkerCluster(options=options)
mc.add_to(m)
m.save('test_map.html')
