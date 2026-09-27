# portfolio

Source for [akshatdhiman.in](https://akshatdhiman.in), served by GitHub Pages from `main`.

The map at the top is real output from
[isochrone-delivery-areas](https://github.com/Akshat120/isochrone-delivery-areas):
5, 10 and 15-minute scooter zones around Hazratganj, Lucknow.
Map data © OpenStreetMap contributors.

## Editing

`index.html` is generated. Edit `src/template.html`, then rebuild:

```bash
python3 src/build.py
```

That inlines the map from `src/map.json` into `index.html`.
