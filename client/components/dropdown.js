import { useEffect, useState } from 'react'
import { pushRequest } from '../pages/api/apiUtils';


const loadData = async (set) => {
  const tags = await pushRequest('/tag', 'GET')
  set(tags)
}

function Dropdown(props) {
  const [tags, setTags] = useState([])
  const [searchTags, setSearchTags] = useState([])
  const [print, setprint] = useState("")

  if (typeof window === "undefined") {
    //bypass ssr
    return null
  } else {
    useEffect(async () => {
      await loadData(setTags)
      return () => {}
    }, []);
  }

  // Declare an array of items
  const items = tags.map((value, idx) => {
    return value.name
  })

  // Handle the change event for the dropdown menu
  const handleChange = (event) => {
    // Get the selected item from the event target
    const selectedItem = event.target.value

    // Add the selected item to the result array
    if (!searchTags.find(elem => elem === selectedItem)){
      searchTags.push(selectedItem)
      setSearchTags(searchTags)
      setprint(searchTags.join(', '))
    }
  }
  return (
    <div style={{
      color:'white',
      textAlign:'center',
      margin: '2vmin',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-evenly',
      flexDirection:'column'
    }}>
      {/* Create the dropdown menu */}
      <select onChange={handleChange}>
        {/* Add options for each item in the items array */}
        {items.map((item) => (
          <option key={item} value={item}>
            {item}
          </option>
        ))}
      </select>

      {/* Display the result array */}
      <div style={{
        color:'white',
        textAlign:'center',
        display: 'flex',
        flexDirection:'column'
      }}>
        Selected tags: {print}
      </div>
    </div>
  )
}

export default Dropdown