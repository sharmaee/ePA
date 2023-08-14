export function generateRandom4DigitNumber() {
  return Math.floor(Math.random() * (9999 - 1000 + 1)) + 1000;
}
