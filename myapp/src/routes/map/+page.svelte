<script>
  import { onMount, onDestroy } from 'svelte';

  let map;

  onMount(async () => {
    const L = await import('leaflet');

    map = L.map('map').setView([0, 0], 2); // Default initial view

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
      maxZoom: 18
    }).addTo(map);

    L.Icon.Default.imagePath = '/leaflet/';

    // Add user markers here
    // Example:
    L.marker([51.505, -0.09]).addTo(map)
      .bindPopup('User 1')
      .openPopup();

    L.marker([40.7128, -74.006]).addTo(map)
      .bindPopup('User 2')
      .openPopup();

    // Add more user markers as needed
  });

  // Cleanup the map when the component is destroyed
  onDestroy(() => {
    if (map) {
      map.remove();
    }
  });
</script>

<style>
  #map {
    height: 400px;
  }
</style>

<main>
  <h1>User Map</h1>
  <div id="map"></div>
</main>
