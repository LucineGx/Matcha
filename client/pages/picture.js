import { useEffect, useState } from "react"
import { pushRequest } from "./api/apiUtils"



export default function Picture (dfghjklsdfgb) {
  const [state, setstate] = useState(0)
  const [images, setImages] = useState([])
  const [user, setUser] = useState({})
  const [file, setFile] = useState({})

  useEffect( () => {
    pushRequest('user/', 'GET')
      .then((data) => setUser(data))
      .catch((reason) => console.error(reason))
  }, [])//change empty array for image
  // console.log(user)

  const changeHandler = (event) => {
    setFile(event.target.files[0])
    console.log(event.target.files[0])
  }

  return (
    <>
      <img src={`data:image/png;base64,${file}`}/>
      <div>
        <input onChange={changeHandler} type="file" id="avatar" name="avatar" accept="image/png, image/jpeg"/>
      </div>
      <button onMouseOver={() => setstate(state+1)} >
        {state}
      </button>
    </>
  )
}