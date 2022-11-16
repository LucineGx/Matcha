const formatBase64Jpeg = (picture) => {
  picture = picture.replace('dataimage', 'data:image')
  picture = picture.replace('/jpegbase64', 'jpeg;base64,')
  return picture
}

export {
  formatBase64Jpeg
}