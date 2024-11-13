from qgis.core import QgsProject, QgsRasterLayer, QgsMultiBandColorRenderer, QgsContrastEnhancement, QgsRasterMinMaxOrigin

# Define the band indices for red, green, and blue
RED_BAND_INDEX = 6  # Adjust to match your raster bands
GREEN_BAND_INDEX = 4
BLUE_BAND_INDEX = 2

# Percentiles for contrast enhancement
MIN_PERCENTILE = 2.0
MAX_PERCENTILE = 98.0

# Process all raster layers in the project
for layer in QgsProject.instance().mapLayers().values():
    if isinstance(layer, QgsRasterLayer):  # Check if it's a raster layer
        print(f"Processing layer: {layer.name()}")
        try:
            # Set the renderer to multiband color if not already set
            if not isinstance(layer.renderer(), QgsMultiBandColorRenderer):
                renderer = QgsMultiBandColorRenderer(layer.dataProvider(), RED_BAND_INDEX, GREEN_BAND_INDEX, BLUE_BAND_INDEX)
                layer.setRenderer(renderer)
            else:
                renderer = layer.renderer()
                renderer.setRedBand(RED_BAND_INDEX)
                renderer.setGreenBand(GREEN_BAND_INDEX)
                renderer.setBlueBand(BLUE_BAND_INDEX)

            # Apply contrast enhancement to each band
            for band in [RED_BAND_INDEX, GREEN_BAND_INDEX, BLUE_BAND_INDEX]:
                # Calculate statistics for the band
                provider = layer.dataProvider()
                stats = provider.bandStatistics(
                    band, QgsRasterMinMaxOrigin.CumulativeCut, MIN_PERCENTILE, MAX_PERCENTILE
                )

                # Set contrast enhancement
                contrast_enhancement = QgsContrastEnhancement(layer.dataProvider().dataType(band))
                contrast_enhancement.setMinimumValue(stats.minimumValue)
                contrast_enhancement.setMaximumValue(stats.maximumValue)
                contrast_enhancement.setContrastEnhancementAlgorithm(QgsContrastEnhancement.StretchToMinimumMaximum)
                renderer.setContrastEnhancement(band - 1, contrast_enhancement)

            # Refresh the layer to apply the changes
            layer.triggerRepaint()
            print(f"Applied RGB bands and contrast enhancement to layer: {layer.name()}")

        except Exception as e:
            print(f"Error processing layer {layer.name()}: {e}")

print("Processing complete.")
