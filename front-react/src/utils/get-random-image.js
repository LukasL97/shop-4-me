import alcohol from '../assets/images/alcohol.jpg'
import bakery from '../assets/images/bakery.jpg'
import frozen from '../assets/images/frozen.jpg'
import fruits from '../assets/images/fruits.jpg'
import meat from '../assets/images/meat.jpg'
import milk from '../assets/images/milk.jpg'
import toilet from '../assets/images/toilet.jpg'
import ready_made_food from '../assets/images/ready_made_food.jpg'
import soft_drinks from '../assets/images/soft_drinks.jpg'

export const getRandomImage = () => {
  const images = [
    alcohol,
    bakery,
    frozen,
    fruits,
    meat,
    milk,
    toilet,
    ready_made_food,
    soft_drinks,
  ]
  let randIndex = Math.floor(Math.random() * images.length)
  let image = images[randIndex]
  return image
}
