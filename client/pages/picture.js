import { useEffect, useState } from "react"
import { pushRequest } from "./api/apiUtils"

export default function Picture () {
  const [user, setUser] = useState({})
  const [file, setFile] = useState("")

  useEffect( () => {
    pushRequest('user/', 'GET')
      .then((data) => setUser(data))
      .catch((reason) => console.error(reason))
  }, [])//change empty array for image

  const toBase64 = file => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  })

  const changeHandler = (event) => {
    const loadedFile = event.target.files[0]
    console.log('files', Object.keys(event.target.files))
    toBase64(loadedFile).then((value) => {
      setFile(value)
      console.log('banan', value)
    })
  }

  return (
    <>
      <div style={{ display: 'flex', flexDirection: 'column' }}>
        <img id='lapin' style={{ borderRadius: '100vh', width: '20vmin', height: '20vmin', margin: '5vmin', position: 'static', left: '30%', display: (!file) ? 'none' : 'flex'}} src={file}/>
        <input onChange={changeHandler} type="file" id="avatar" name="avatar" accept="image/png, image/jpeg" placeholder="lol"/>
        <button onClick={() => {
          const data = new FormData()
          data.append('main', '1')
          data.append('picture', file)
          console.log('type:', typeof file)
          pushRequest('user/picture', 'POST', data, {isText:true})
            .then((value) => console.log(value))
            .catch((error) => console.error(error))
        }}>send nude</button>
      </div>
    </>
  )
}