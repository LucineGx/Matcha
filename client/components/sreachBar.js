import React, { useEffect, useState } from "react";
import { useRouter } from "next/router";
import { Input, Slider } from "antd";
import { toast } from "react-toastify";
import { pushRequest } from "../pages/api/apiUtils";
import Dropdown from "./dropdown";
import ChatPopup from "../pages/popupchat";
import SearchEngine from "./searchEngine";

const { Search } = Input;

const notify = (txt) => toast(txt)
function SearchBar() {
  const router = useRouter()

  const [ageMin, setAgeMin] = useState(18)
  const [ageMax, setAgeMax] = useState(150)
  const [publicPopularityMin, setPublicPopularityMin] = useState(0)
  const [publicPopularityMax, setPublicPopularityMax] = useState(100)
  const [tags, setTags] = useState([])
  const [distance, setDistance] = useState(50)

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
        setAgeMin(value[0])
        setAgeMax(value[1])
        break
      case 'public_popularity':
        setPublicPopularityMin(value[0])
        setPublicPopularityMax(value[1])
        break;
      case 'distance':
        setDistance(value)
        break;
      default:
        break;
    }
  };

  return (
    <>
      <div style={{
        display: 'flex',
        padding: '2vmin',
        justifyContent: 'space-between',
        flexDirection:'column'
      }}>
        <SearchEngine current={tags} updateFunction={setTags}/>
        <button onClick={() => {
          console.log('tags:', tags)
        }}>pouette</button>
      </div>
      {/* <ChatPopup/> */}
      <div style={{
        color: 'white'
        }}
      >
        { makeSilder('age', 18, 200, onChange, {min:ageMin, max:ageMax}, 'Years old' ) }
        { makeSilder('public_popularity', 0, 100, onChange, {min:publicPopularityMin, max:publicPopularityMax}, '%' ) }
        { makeSilder('distance', null, 1000, onChange, distance, 'Km') }
      </div>
    </>
  )
}

function makeSilder(name, min, max, onChangeCallBack, inputValue, unity) {
  //range silder
  if (min != null && max != null) {
    return  (
      <div style={{display: 'flex', margin: '1vmin', flexDirection: 'column'}}>
        <p style={{ width: '100%', color: 'white', margin: '1vmin', flexDirection: 'row' }}>
          {`${name}: ${inputValue.min} ~ ${inputValue.max} ${unity}`}
        </p>
        <Slider
          id={name}
          style={{ width: '20vmax', margin: '1vmax' }}
          min={min}
          max={max}
          range
          defaultValue={[inputValue.min,inputValue.max]}
          onChange={
            (value) => (onChangeCallBack(name, value))
          }
        />
      </div>
    )
  }
  //input silder
  return  (
    <div
      style={{
        display: 'flex',
        margin: '1vmin',
        flexDirection: 'column'
      }}
    >
      <p style={{ width: '100%', color: 'white', margin: '1vmin', flexDirection: 'row' }}>
        {`${name}: ≤ ${inputValue} ${unity}`}
      </p>
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

const youWillDieAlone = () => notify('no needs to be more spesific you\'ll die alone anyway')

export default SearchBar;
