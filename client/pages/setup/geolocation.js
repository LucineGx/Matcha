let geolocation = {
  latitude: null,
  longitude: null,
  city: '',
  country: ''
}
const sleep = ms => new Promise(r => setTimeout(r, ms))


function sucess(position) {
  geolocation.latitude = position.coords.latitude
  geolocation.longitude = position.coords.longitude
  console.log('chrom')
  return geolocation
}

function error(err) {
  console.log('2', err)
}

const options = {
  enableHighAccuracy: true,
  maximumAge: 30000,
  timeout: 27000
}

export async function getGeolocation() {
if ('geolocation' in navigator) {
  navigator.geolocation.getCurrentPosition(sucess, error, options)
}
await sleep(1000)
console.log('current', geolocation)
if (geolocation.latitude == null) {
  try {
    const res = await fetch("https://ipapi.co/json/")
    const data = await res.json()
    geolocation.latitude = (!geolocation.latitude) ? data.latitude : geolocation.latitude
    geolocation.longitude = (!geolocation.longitude) ? data.longitude : geolocation.longitude
    geolocation.city = data.city
    geolocation.country = data.country
    console.log('api')
  } catch (e) {
    // throw new Error(e)
  }
}
return geolocation
}