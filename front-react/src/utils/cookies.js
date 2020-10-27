export const deleteCookie = () => {
  const now = new Date()
  document.cookie = `access_token=; expires=${now}; path=/;`
}

export const parseCookies = () => {
  const cookieObj = {}
  if (!document.cookie)
  	return cookieObj
  const cookiesArr = document.cookie.split(';').map((item) => item.split('='))
  for (const [key, value] of cookiesArr) {
    cookieObj[key.trim()] = value.trim()
  }
  return cookieObj
}
