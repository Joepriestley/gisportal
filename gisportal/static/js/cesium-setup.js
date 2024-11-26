// cesium ion token

Cesium.Ion.defaultAccessToken ='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI3OWE3ZmFhOS01M2MzLTRiMWUtODI0ZS05YmJjZjI0ZGYzZDEiLCJpZCI6MjQxNTkyLCJpYXQiOjE3MjYzMDg1Nzl9.p3LFJJ7_1ZYfrf7MgCswSWiJONwnxhBjiO8TymV4NOs'

// Fetch Cesium Ion asset details from the Django backend
async function fetchCesiumAsset() {
    try {
        const response = await fetch('/cesium-ion/'); // Adjust URL if needed
        if (!response.ok) {
            throw new Error('Failed to fetch asset details');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching Cesium asset details:', error);
    }
}

// Initialize CesiumJS Viewer and load point cloud
async function initializeCesium() {
    // Create a CesiumJS viewer
    const viewer = new Cesium.Viewer('cesiumContainer', {
        terrainProvider: Cesium.createWorldTerrain(), // Optional: Adds real-world terrain
        animation: false, // Disable animation controls
        timeline: false, // Disable timeline
        baseLayerPicker: false, // Disable base layer picker
    });

    // Fetch and display the point cloud
    try {
        const assetDetails = await fetchCesiumAsset();
        if (!assetDetails) {
            console.error('No asset details found. Ensure the backend is returning the correct data.');
            return;
        }

        const { asset_id, access_token } = assetDetails;

        // Load point cloud using Cesium Ion asset details
        const pointCloud = viewer.scene.primitives.add(
            new Cesium.Cesium3DTileset({
                url: Cesium.IonResource.fromAssetId(asset_id, { accessToken: access_token }),
            })
        );

        // Zoom to the point cloud when it is ready
        pointCloud.readyPromise.then(() => {
            viewer.zoomTo(pointCloud);
        }).catch((error) => {
            console.error('Error loading point cloud:', error);
        });
    } catch (error) {
        console.error('Error initializing Cesium:', error);
    }
}

// Execute Cesium initialization
initializeCesium();
