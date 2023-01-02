import React, { useEffect, useState } from "react";
import { useRouter } from "next/router";
import { Input, Slider } from "antd";
import { toast } from "react-toastify";
import { pushRequest } from "../pages/api/apiUtils";
import Dropdown from "./dropdown";
import ChatPopup from "../pages/popupchat";

const { Search } = Input;

const notify = (txt) => toast(txt)
function SearchBar() {
  const router = useRouter();
  const [filters, setFilters] = useState({
    age: {
      min: 18,
      max: 200,
    },
    popularity: {
      min: 0,
      max: 0
    },
    tags: [],
  })
  const [inputValue, setInputValue] = useState(1000);

  // const onSearch = (value) => {
  //   router.push({
  //     pathname: "/search",
  //     query: { q: value, min: minValue, max: maxValue },
  //   });
  //   // console.log('lol',router.query)
  // };

  const onChange = (name, value) => {
    switch (name) {
      case 'age':
        setFilters(Object.assign(filters, { age: { min: value[0], max: value[1] } }))
        break;
      case 'public_popularity':
        setFilters(Object.assign(filters, { popularity: { min: value[0], max: value[1] } }))
        break;
      case 'distance':
        setInputValue(value)
        break;
      default:
        break;
    }
  };

  return (
    <>
      <div style={{display: 'flex', margin: '1vmin',}}>
        {/* <Search placeholder="Enter tags search" onSearch={() => notify('no needs to be more spesific you\'ll die alone anyway')} /> */}
        <Dropdown/>
      </div>
      <ChatPopup/>
      { makeSilder('age', 18, 200, onChange) }
      { makeSilder('public_popularity', 0, 100, onChange) }
      { makeSilder('distance', null, 1000, onChange, inputValue) }
    </>
  );
}

function makeSilder(name, min, max, onChangeCallBack, inputValue) {
  if (min != null && max != null) {
    return  (
      <div style={{display: 'flex', margin: '1vmin', flexDirection: 'column'}}>
        <p style={{ width: '1vmax', color: 'white', margin: '1vmin' }}>{name}</p>
        <Slider id={name} style={{ width: '20vmax', margin: '1vmax' }} min={min} max={max} range defaultValue={[min,max]} onChange={
          (value) => (onChangeCallBack(name, value))
        } />
      </div>
    )
  }
  return  (
    <div style={{display: 'flex', margin: '1vmin', flexDirection: 'column'}}>
      <p style={{ width: '1vmax', color: 'white', margin: '1vmin' }}>{name}</p>
      <Slider
          id={name}
          min={0}
          max={max}
          style={{ width: '20vmax', margin: '1vmax' }}
          onChange={(val)=>{onChangeCallBack(name, val)}}
          value={inputValue}
        />
    </div>
  )
}

export default SearchBar;
