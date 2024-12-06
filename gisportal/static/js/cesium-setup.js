document.addEventListener('DOMContentLoaded', () => {
    const toggleIcon = document.getElementById('toggleIcon');
    const assetList = document.getElementById('assetList');

    toggleIcon.addEventListener('click', () => {
        const isVisible = assetList.style.display === 'block';
        assetList.style.display = isVisible ? 'none' : 'block';

        // Toggle the icon between open and close states
        toggleIcon.className = isVisible ? 'fas fa-list' : 'fas fa-times'; // List icon or Close icon
    });
});

async function fetchCesiumToken() {
    const response = await fetch('http://127.0.0.1:9008/globetudes/api/cesium-ion-token/');
    if (response.ok) {
        const data = await response.json();
        return data.access_token;
    } else {
        console.error("Failed to fetch Cesium access token:", response.statusText);
        return null;
    }
}

async function fetchCesiumAssets() {
    const response = await fetch('http://127.0.0.1:9008/globetudes/cesium-ion/');
    if (response.ok) {
        return await response.json();
    } else {
        console.error("Failed to fetch Cesium assets:", response.statusText);
        return { items: [] };
    }
}

async function initializeCesium() {
    const cesiumAccessToken = await fetchCesiumToken();
    if (!cesiumAccessToken) {
        console.error("No Cesium Ion token received.");
        return;
    }

    Cesium.Ion.defaultAccessToken = cesiumAccessToken;

    const assetData = await fetchCesiumAssets();

    const viewer = new Cesium.Viewer('cesiumContainer', {
        terrainProvider: Cesium.createWorldTerrain(),
        animation: false,
        timeline: false,
        baseLayerPicker: false,
    });

    const loadedAssets = {};
    const assetList = document.getElementById('assetList');

    assetData.items.forEach(asset => {
        const assetId = asset.id;
        const assetName = asset.name;

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = `asset-${assetId}`;
        checkbox.dataset.assetId = assetId;

        const label = document.createElement('label');
        label.htmlFor = `asset-${assetId}`;
        label.innerText = ` ${assetName}`;

        const listItem = document.createElement('div');
        listItem.appendChild(checkbox);
        listItem.appendChild(label);
        assetList.appendChild(listItem);

        checkbox.addEventListener('change', async function () {
            const isChecked = this.checked;

            if (isChecked) {
                const tileset = viewer.scene.primitives.add(
                    new Cesium.Cesium3DTileset({
                        url: Cesium.IonResource.fromAssetId(assetId),
                    })
                );

                await tileset.readyPromise;
                viewer.zoomTo(tileset);

                loadedAssets[assetId] = tileset;
            } else {
                const tileset = loadedAssets[assetId];
                if (tileset) {
                    viewer.scene.primitives.remove(tileset);
                    delete loadedAssets[assetId];
                }
            }
        });
    });
}

initializeCesium();
