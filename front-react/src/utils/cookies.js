export const deleteCookie = () => {
  const now = new Date()
  document.cookie = `access_token=; expires=${now}; path=/;`
}

export const parseCookies = () => {
  const cookieObj = {}
  const cookiesArr = document.cookie.split(';').map((item) => item.split('='))
  for (const [key, value] of cookiesArr) {
    cookieObj[key] = value.trim()
    // some mine change 
  }
  return cookieObj
}
