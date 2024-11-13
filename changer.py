# Get the active layer
layer = iface.activeLayer()  # Ensure the layer is selected in the Layers Panel

# Start editing the layer
layer.startEditing()

# Iterate only through selected features
for feature in layer.getFeatures():
    # Check if the 'class' attribute is 'Crop'
    if feature['class'] == 'Crop':
        # Update the 'class' field to 'Trees'
        feature['class'] = 'Trees'
        # Apply the update to the feature in the layer
        layer.updateFeature(feature)

# Save the changes
layer.commitChanges()

print("Selected attribute values updated successfully.")

# Get both layers
source_layer = QgsProject.instance().mapLayersByName("Intersection")[0]  # Replace with your source layer name
target_layer = QgsProject.instance().mapLayersByName("LULC_MURAN'GA_2022")[0]  # Replace with your target layer name

# Start editing the target layer
target_layer.startEditing()

# Create a dictionary from the source layer with fid as the key and class as the value
class_values = {feature.id(): feature['class'] for feature in source_layer.getFeatures()}

# Iterate over each feature in the target layer
for target_feature in target_layer.getFeatures():
    # Check if the fid in the target layer exists in the source layer dictionary
    if target_feature.id() in class_values:
        # Get the new class value from the source layer
        new_class_value = class_values[target_feature.id()]
        
        # Set the new class value in the target feature
        target_feature['class'] = new_class_value
        # Update the feature in the target layer
        target_layer.updateFeature(target_feature)

# Commit changes to save the updates
target_layer.commitChanges()

print("Class values updated successfully in the target layer.")

