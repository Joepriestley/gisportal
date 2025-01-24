document.addEventListener('DOMContentLoaded', () => {
    const assetToggle = document.getElementById('assetToggle');
    const assetList = document.getElementById('assetList');

    // Toggle asset list visibility
    if (assetToggle && assetList) {
        assetToggle.addEventListener('click', () => {
            const isVisible = assetList.style.display === 'block';
            assetList.style.display = isVisible ? 'none' : 'block';
        });
    } else {
        console.warn("Asset toggle or asset list not found in DOM.");
    }
});

// Fetch Cesium Ion Token
async function fetchCesiumToken() {
    try {
        const response = await fetch('http://127.0.0.1:9008/globetudes/api/cesium-ion-token/');
        if (!response.ok) throw new Error(response.statusText);
        const data = await response.json();
        return data.access_token;
    } catch (error) {
        console.error("Failed to fetch Cesium access token:", error.message);
        return null;
    }
}

// Fetch Cesium Assets
async function fetchCesiumAssets() {
    try {
        const response = await fetch('http://127.0.0.1:9008/globetudes/cesium-ion/');
        if (!response.ok) throw new Error(response.statusText);
        return await response.json();
    } catch (error) {
        console.error("Failed to fetch Cesium assets:", error.message);
        return { items: [] };
    }
}

// Fetch GeoJSON Data
async function fetchGeojsonData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(response.statusText);
        return await response.json();
    } catch (error) {
        console.error("Failed to fetch GeoJSON data:", error.message);
        return null;
    }
}
/// selected layer
let selectedLayer = null;

// Visualize GeoJSON Data
async function visualiseData(viewer, geojsonUrl, defaultColor, selectedColor) {
    const geojsonData = await fetchGeojsonData(geojsonUrl);
    if (geojsonData) {
        try {
            const dataSource = await viewer.dataSources.add(
                Cesium.GeoJsonDataSource.load(geojsonData, {
                    stroke: defaultColor,
                    fill: defaultColor.withAlpha(0.6),
                    clampToGround: true,
                    outline: true,
                    outlineColor: Cesium.Color.BLACK,
                })
            );

            // Add click handler to toggle color
            const handler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas);

            handler.setInputAction((click) => {
                const pickedObject = viewer.scene.pick(click.position);

                if (Cesium.defined(pickedObject) && Cesium.defined(pickedObject.id)) {
                    const entity = pickedObject.id;

                    if (selectedLayer && selectedLayer !== entity) {
                        // Reset the color of the previously selected layer
                        selectedLayer.polygon.material = defaultColor;
                    }

                    // Update the selected layer
                    selectedLayer = entity;

                    // Change color of the selected layer
                    entity.polygon.material = selectedColor;
                }
            }, Cesium.ScreenSpaceEventType.LEFT_CLICK);

            viewer.zoomTo(dataSource);
        } catch (error) {
            console.error("Failed to load GeoJSON data:", error.message);
        }
    }
}


// GeoJSON URLs
const forestGeoJSONUrl = 'http://127.0.0.1:9008/globetudes/forest/';
const parcelGeoJSONUrl = 'http://127.0.0.1:9008/globetudes/parcelle/';
const cantonGeoJSONUrl = 'http://127.0.0.1:9008/globetudes/canton/';

// Initialize Cesium Viewer and Load Assets
async function initializeCesium() {
    // Fetch Cesium Ion Token
    const cesiumAccessToken = await fetchCesiumToken();
    if (!cesiumAccessToken) {
        console.error("No Cesium Ion token received. Initialization aborted.");
        return;
    }

    // Set Cesium Ion default token
    Cesium.Ion.defaultAccessToken = cesiumAccessToken;

    // Create Cesium Viewer
    const viewer = new Cesium.Viewer('cesiumContainer', {
        terrainProvider: Cesium.createWorldTerrain(),
        animation: false,
        timeline: false,
        baseLayerPicker: true,
    });

    // Set initial camera view
    viewer.camera.setView({
        destination: Cesium.Cartesian3.fromDegrees(-13, 27.7, 4900000),
    });

    // Fetch and Load Assets
    const assetData = await fetchCesiumAssets();
    const loadedAssets = {};
    const assetList = document.getElementById('assetList');

    assetData.items.forEach((asset) => {
        const { id: assetId, name: assetName } = asset;

        // Create asset checkbox
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = `asset-${assetId}`;
        checkbox.dataset.assetId = assetId;

        // Create asset label
        const label = document.createElement('label');
        label.htmlFor = `asset-${assetId}`;
        label.innerText = ` ${assetName}`;

        // Append checkbox and label to asset list
        const listItem = document.createElement('div');
        listItem.appendChild(checkbox);
        listItem.appendChild(label);
        assetList.appendChild(listItem);

        // Handle asset toggle
        checkbox.addEventListener('change', async function () {
            const isChecked = this.checked;

            if (isChecked) {
                try {
                    const tileset = viewer.scene.primitives.add(
                        new Cesium.Cesium3DTileset({
                            url: Cesium.IonResource.fromAssetId(assetId),
                        })
                    );
                    await tileset.readyPromise;
                    viewer.zoomTo(tileset);
                    loadedAssets[assetId] = tileset;
                } catch (error) {
                    console.error(`Failed to load asset ${assetName}:`, error.message);
                }
            } else {
                const tileset = loadedAssets[assetId];
                if (tileset) {
                    viewer.scene.primitives.remove(tileset);
                    delete loadedAssets[assetId];
                }
            }
        });
    });

    // Visualize GeoJSON Data
    visualiseData(viewer, forestGeoJSONUrl, Cesium.Color.GREEN, Cesium.Color.BLACK);
    visualiseData(viewer, parcelGeoJSONUrl, Cesium.Color.BLUE, Cesium.Color.ORANGE);
    visualiseData(viewer, cantonGeoJSONUrl, Cesium.Color.RED, Cesium.Color.MAGENTA);
}

initializeCesium();
