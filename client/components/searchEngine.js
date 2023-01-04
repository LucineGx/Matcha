import { useEffect, useState } from 'react'
import { pushRequest } from '../pages/api/apiUtils';
import { AutoComplete } from 'antd'

const loadData = async (set) => {
  const tags = await pushRequest('/tag', 'GET')
  set(tags)
}

function SearchEngine(props) {
  const [tags, setTags] = useState([])
  // const [searchTags, setSearchTags] = useState(props.current)
  const [print, setprint] = useState("")
  const {current, updateFunction} = props

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
    return {value: value.name}
  })

  // Handle the change event for the dropdown menu
  const handleChange = (value) => {}

  const handleSearch = (value, target) => {
    const selectedItem = value

    // // Add the selected item to the result array
    if (!current.find(elem => elem === selectedItem)){
      current.push(selectedItem)
      updateFunction(current)
      setprint(current.join(', '))
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
      {/* <select onChange={handleChange}> */}
      {
        /* Add options for each item in the items array */
        // items.map((item) => (
        //   <option key={item} value={item}>
        //     {item}
        //   </option>
        // ))
      }
      {/* </select> */}

      <AutoComplete
        placeholder="Enter tags search"
        options={items}
        style={{
          width: '200px',
          color: 'black'
        }}
        filterOption={(inputValue, option) =>
          option.value.toUpperCase().indexOf(inputValue.toUpperCase()) !== -1
        }
        onSelect={handleSearch}
        onChange={handleChange}
      />

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

export default SearchEngine