import { useEffect, useRef, useState } from "react"
import { pushRequest } from "../../pages/api/apiUtils"
import { formatBase64Jpeg } from "../../pages/api/formatBase64Jpeg"
import { toast } from 'react-toastify'

const notify = (txt) => toast(txt)

/** @typedef {import('../../pages/type/userInfo').UserInfo} UserInfo */

/**
 * @type { React.CSSProperties }
 */
const style = {
  borderRadius: '100vh',
  width: '20vmin',
  height: '20vmin',
  margin: '5vmin',
  position: 'static',
  left: '30%'
}
const styleB = {
  borderRadius: '1vh',
  width: '20vmin',
  height: '20vmin',
  // margin: '1vmin',
  position: 'static',
  // left: '30%'
}

const toBase64 = file => new Promise((resolve, reject) => {
  const reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onload = () => resolve(reader.result);
  reader.onerror = error => reject(error);
})

/** @param {import("react").Dispatch<any>} fn */
const loadPictures = async (fn) => {
  const pic = await pushRequest(`user/pictures`, 'GET')
  fn(pic)
  console.log(pic)
}

export default function Picture (props) {
  let oldPicture = props.photo
  let newPicture = []
  // console.log('koala', props)
  const [willUpdate, setWillUpdate] = useState(0)
  const [currentPic, setCurrentPic] = useState(oldPicture)

  useEffect(async () => {
    await loadPictures(setCurrentPic)
  }, [willUpdate])

  const changeHandler = async (event) => {
    event.preventDefault()
    const loadedFile = event.target.files[0]
    let toLoad = await toBase64(loadedFile)
    newPicture.push(toLoad)
    // debugger
    uploadOneOrManyPicture(toLoad)
  }

  const subPicture = () => {
    if (props.main === true || (!oldPicture.length && !newPicture.length))
      return null
    const RenderedPictures = currentPic.map((value) => {
      if (value.main === 0) {
        const divRef = 'container'+value.id
        const buttonRef = 'deleteButton'+value.id
        const picRef = 'picture'+value.id
        return (
          <div
            id={divRef}
            style={{display: 'flex', flexDirection: 'row', marginInline: '1vmax'}}
            onMouseOver={(event) => {
              //old school js go brrrr
              document.getElementById(picRef).style.opacity = '30%'
              document.getElementById(buttonRef).style.display = null
            }}
            onMouseLeave={(event) => {
              document.getElementById(picRef).style.opacity = '100%'
              document.getElementById(buttonRef).style.display = 'none'
            }}
          >
            <div style={/** @type { React.CSSProperties } */{display:'flex', flexDirection:'column'}}>
              <span
                id={buttonRef}
                style={{position: 'relative', left:'10vmax', display: 'none', color: 'red', fontSize: '2vmin', cursor: 'pointer'}}
                onClick={async () => {
                  const response = await pushRequest('user/picture/' + value.id, 'DELETE')
                  console.log(response)
                  if (response && Array.isArray(response) && currentPic && response.length < currentPic.length)
                    setWillUpdate(willUpdate+1)
                }}
              >
                X
              </span>
              <img
                id={picRef}
                style={{display: "flex", ...styleB}}
                src={value.picture}
              />
            </div>
          </div>
        )
      }
    })
    return (
      <div style={{ display: "flex" }}>
        {RenderedPictures}
      </div>
    )
  }

  const chosePicture = () => {
    let moreStyles = {}
    if (props.main === true){
      const mainPicture = currentPic.find(value => value.main === 1 )
      console.log('currentPic', currentPic, !!mainPicture)
      if (mainPicture){
        return (
          <img
            id="lapun"
            style={{...moreStyles, ...style, display: 'flex'}}
            src={mainPicture.picture}
            onMouseOver={(event) => {
              event.preventDefault()
              moreStyles.opacity = '50%'
            }}
          />
        )
      }
    }
    return subPicture()
  }

  /**
   * @param {string} picture - base64 url encoded string
   * @param {boolean} [isMain] - base64 url encoded string
   */
  const pushPictures = (picture, isMain = false) => {
    const data = new FormData()
    if (props.main === true)
      data.append('main', '1')
    else
      data.append('main', '0')
    data.append('picture', picture)
    pushRequest('user/picture', 'POST', data, {isText:true})
      .then(() => {
        setWillUpdate(willUpdate + 1)
      })
      .catch((error) => console.error(error))
  }

  const uploadOneOrManyPicture = (toLoad) => {
    // debugger
    if (currentPic.length >= 5)
      return notify('maximum of 5 picture (1 profile picture + 4')
    if (props.main === true){
      pushPictures(toLoad, true)
    } else if (newPicture) {
      for (const pic of newPicture) {
        pushPictures(pic)
      }
    }
  }

  const renderUploadInput = (props) => {
    if (props.canUpload === true){
      return (
        <>
          <label htmlFor='avatar'
            style={{
              border: '1vmin ridge rgba(211, 220, 50, .6)',
              background: '#DCDDDF',
              borderRadius: '1vmin',
              fontSize: '1vmax',
              cursor: 'pointer'
            }}
          >choisir un nude</label>
          <input
            onChange={changeHandler}
            type="file"
            id="avatar"
            name="avatar"
            accept="image/png, image/jpeg"
            placeholder="lol"
            style={{
              // background: 'blue',
              display:'none'
            }}
          />
          {/* <button onClick={uploadOneOrManyPicture}>
            send nude
          </button> */}
        </>
      )
    }
  }

  return (
    <>
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          margin: '1.5vmin'
        }}
      >
        {chosePicture()}
        {renderUploadInput(props)}
      </div>
    </>
  )
}