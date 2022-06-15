from flask import Flask,render_template
import folium
from icons import antenna, car



app = Flask(__name__)

@app.route('/')
def map_func():
    m = folium.Map(location=[40.631491, -8.656481], zoom_start=75, control_scale=True)

    #RSU Marker
    folium.Marker(
        location=[40.631491, -8.656481],
        popup="<b>RSU1</b>",
        icon=antenna
    ).add_to(m)

    #OBU Marker
    folium.Marker(
        location=[40.631662, -8.656547],
        popup="<b>OBU1</b>",
        icon=car
    ).add_to(m)


    return m._repr_html_()


if __name__ == '__main__':
    app.run(debug = True)    