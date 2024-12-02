async function fetchCesiumToken() {
    // Fetch the token from your Django backend
    const response = await fetch('http://127.0.0.1:9008/globetudes/api/cesium-ion-token/'); // Adjust your API endpoint URL
    if (response.ok) {
        const data = await response.json();
        return data.access_token;  // Extract the token from the response
    } else {
        console.error("Failed to fetch Cesium access token:", response.statusText);
        return null; // Return null if there was an error
    }
}

async function fetchCesiumAssets() {
    const response = await fetch('http://127.0.0.1:9008/globetudes/cesium-ion/'); // Adjust API endpoint URL
    if (response.ok) {
        return await response.json();
    } else {
        console.error("Failed to fetch Cesium assets:", response.statusText);
        return { items: [] };
    }
}

async function initializeCesium(){
    // Fetch Cesium Ion access token from backend
    const cesiumAccessToken = await fetchCesiumToken();
    if (!cesiumAccessToken) {
        console.error("No Cesium Ion token received.");
        return;
    }

    // Set Cesium Ion access token dynamically
    Cesium.Ion.defaultAccessToken = cesiumAccessToken;

    // Fetch Cesium assets from the backend
    const assetData = await fetchCesiumAssets();

    // Initialize Cesium viewer
    const viewer = new Cesium.Viewer('cesiumContainer', {
        terrainProvider: Cesium.createWorldTerrain(),
        animation: false,
        timeline: false,
        baseLayerPicker: true,
    });

    // Container for loaded assets
    const loadedAssets = {};

    // Populate the asset list in the UI
    const assetList = document.getElementById('assetList');
    assetData.items.forEach(asset => {
        const assetId = asset.id;
        const assetName = asset.name;

        // Create a checkbox for each asset
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = `asset-${assetId}`;
        checkbox.dataset.assetId = assetId;

        // Create a label for the checkbox
        const label = document.createElement('label');
        label.htmlFor = `asset-${assetId}`;
        label.innerText = ` ${assetName}`;

        // Append checkbox and label to the asset list
        const listItem = document.createElement('div');
        listItem.appendChild(checkbox);
        listItem.appendChild(label);
        assetList.appendChild(listItem);

        // Add event listener for toggling assets
        checkbox.addEventListener('change', async function () {
            const isChecked = this.checked;
            const assetId = this.dataset.assetId;

            if (isChecked) {
                // Load the asset
                const tileset = viewer.scene.primitives.add(
                    new Cesium.Cesium3DTileset({
                        url: Cesium.IonResource.fromAssetId(assetId),
                    })
                );

                // Zoom to the asset when ready
                await tileset.readyPromise;
                viewer.zoomTo(tileset);

                // Store the loaded tileset
                loadedAssets[assetId] = tileset;
            } else {
                // Unload the asset
                const tileset = loadedAssets[assetId];
                if (tileset) {
                    viewer.scene.primitives.remove(tileset);
                    delete loadedAssets[assetId];
                }
            }
        });
    });
}

// Execute Cesium initialization
initializeCesium();
