import { useEffect, useState } from 'react'
import { pushRequest } from '../pages/api/apiUtils';


const loadData = async (set) => {
  const tags = await pushRequest('/tag', 'GET')
  set(tags)
}

function Dropdown(props) {
  // Declare a state variable for the selected item and set its initial value to null
  const [selected, setSelected] = useState(null)

  const [tags, setTags] = useState([]);
  const [searchTags, setSearchTags] = useState([]);
  const [search, setSearch] = useState([]);
  // Declare the result array
  const result = []

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

    // Update the state variable with the selected item
    setSelected(selectedItem)

    // Add the selected item to the result array
    if (!searchTags.find(elem => elem === selectedItem)){
      searchTags.push(selectedItem)
      setSearchTags(searchTags)
    }
    console.log('selectedItem', selectedItem, 'result', searchTags)
  }

  return (
    <div>
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
      <div style={{color:'white'}}>
        Result: {result.join(', ')}
      </div>
    </div>
  )
}

export default Dropdown