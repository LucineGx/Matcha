import { useEffect, useRef, useState } from "react"
import { pushRequest } from "./api/apiUtils"
import { formatBase64Jpeg } from "./api/formatBase64Jpeg"

/** @typedef {import('./type/userInfo').UserInfo} UserInfo */

/**
 * @type { React.CSSProperties }
 */
const style = {borderRadius: '100vh', width: '20vmin', height: '20vmin', margin: '5vmin', position: 'static', left: '30%'}
const styleB = {borderRadius: '1vh', width: '20vmin', height: '20vmin', margin: '1vmin', position: 'static', left: '30%'}

const toBase64 = file => new Promise((resolve, reject) => {
  const reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onload = () => resolve(reader.result);
  reader.onerror = error => reject(error);
})

export default function Picture (props) {
  /** @type {UserInfo} */
  let userInfo = {}
  const [user, setUser] = useState(userInfo)
  const [profilePicture, setProfilePicture] = useState("")
  const [folder, setFolder] = useState([])
  const lol = useRef(true)
  const pute = Object.keys(user).length
  require('react-dom')
  window.lol2 = require('react')
  console.log("test:", window.lol1 === window.lol2)
  if (pute === 0){
    useEffect( () => {
      pushRequest('user/', 'GET')
        .then((data) => {
          userInfo = data
          if (data.picture) {
            const photo = formatBase64Jpeg(data.picture)
            userInfo.picture = photo
          }
        })
        .catch((reason) => console.error(reason))
      if (user && user.id) {
        pushRequest(`user/${user.id}/pictures`)
          .then((data) => {
            console.log('datatatatatata', data)
          })
          .catch((reason) => console.error('reason: PUTE', reason))
      }
      return () => {
        lol.current = false
        setUser(userInfo)
        setProfilePicture("")
        setFolder([])
      }
    }, [])//change empty array for image
  }

  const changeHandler = (event) => {
    const loadedFile = event.target.files[0]
    // console.log('files', Object.keys(event.target.files))
    toBase64(loadedFile).then((value) => {
      if (props.main === true){
        setProfilePicture(value)
        // console.log('banan', value)
      } else {
        setFolder([...folder, value])
      }
    })
  }

  const subPicture = () => {
    if (props.main === true || !folder?.length)
      return null
    const pictures = folder.map((value, index) => {
      return (
        <img
          id={'picture'+index}
          style={{ ...styleB, display: 'flex'}}
          src={value}
        />
      )
  })
    return (
      <div style={{display: "flex", }}>
        {pictures}
      </div>
    )
  }

  const chosePicture = () => {
    if (props.main === true){
      console.log('chalom', profilePicture, user)
      return <img id='lapun' style={{ ...style, display: 'flex'}} src={profilePicture}/>
    }
    return subPicture()
  }

  /**
   * @param {string} picture - base64 url encoded string
   * @param {boolean} [isMain] - base64 url encoded string
   */
  const pushPictures = (picture, isMain = false) => {
    const data = new FormData()
    if (isMain === false)
      data.append('main', '0')
    else
      data.append('main', '1')
    data.append('picture', picture)
    pushRequest('user/picture', 'POST', data, {isText:true})
      .then((value) => console.log(value))
      .catch((error) => console.error(error))
  }

  return (
    <>
      <div style={{ display: 'flex', flexDirection: 'column' , margin: '1.5vmin'}}>
        <img id='lapun' style={{ ...style, display: 'flex'}} src={user.picture}/>
        {chosePicture()}
        <input onChange={changeHandler} type="file" id="avatar" name="avatar" accept="image/png, image/jpeg" placeholder="lol"/>
        <button onClick={() => {
          if (props.main === true){
            pushPictures(profilePicture, true)
          } else if (folder) {
            for (const pic of folder) {
              pushPictures(pic)
            }
          }
        }}>send nude</button>
      </div>
    </>
  )
}