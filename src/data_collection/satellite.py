import ee
import geemap.core as geemap

ee.Initialize(project="aquaticweeds7");
Map = geemap.Map();

image = ee.Image(ee.ImageCollection('LANDSAT/LC08/C02/T1_TOA')
  .filterDate('2017-01-01', '2017-12-31')
  .filterBounds(ee.Geometry.Point(27.8569, -25.7381))
  .sort('CLOUD_COVER')
  .first());

rgb = image.select('B4', 'B3', 'B2');
pan = image.select('B8');

huesat = rgb.rgbToHsv().select('hue', 'saturation');
upres = ee.Image.cat(huesat, pan).hsvToRgb();

Map.setCenter(27.8569, -25.7381, 13);

Map.addLayer(rgb, {max: 0.3}, 'Original');
Map.addLayer(upres, {max: 0.3}, 'Pansharpened');

Map