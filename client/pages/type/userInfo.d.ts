/** @type {UserInfo} */

export interface UserInfo {
  age: number
  created_on: Date | string
  custom_localisation: 0 | 1
  email: string
  first_name: string
  gender: 'male' | 'female' | 'other' | null
  id: number
  last_name: string
  lat: number
  lon: number
  public_popularity: string
  search_female: 0 | 1
  search_male: 0 | 1
  search_other: 0 | 1
  short_bio: string
  username: string
}