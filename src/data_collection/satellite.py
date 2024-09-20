import ee;

ee.Authenticate();
ee.Initialize(project="aquaticweeds7");

print(ee.String('Hello from the Earth Engine servers!').getInfo())