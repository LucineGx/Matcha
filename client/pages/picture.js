import { useEffect, useState } from "react"
import { pushRequest } from "./api/apiUtils"



export default function Picture (dfghjklsdfgb) {
  const [state, setstate] = useState(0)
  const [images, setImages] = useState([])
  const [user, setUser] = useState({})
  useEffect( () => {
    pushRequest('user/', 'GET')
      .then((res) => res.json())
      .then((data) => setUser(data))
      .catch((reason) => console.error(reason))
  }, [user])//change empty array for image
  console.log(user)



  return (
    <>
      <button onMouseOver={() => setstate(state+1)} >
        {state}
      </button>
    </>
  )
}