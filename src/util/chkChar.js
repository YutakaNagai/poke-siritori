// 使用可能文字のチェック用js
import { NAME, FIRST_CHAR, FIRST_CHAR_ADDITION } from "./const.js";

// 50音のみ
const filteredFirstChar = FIRST_CHAR.filter((char) => {
  return NAME.some((poke) => {
    return poke.charAt(0) === char;
  });
});

console.log("filteredFirstChar :>> ", filteredFirstChar);

// 追加セット（拗音等）
const filteredFirstCharAddition = FIRST_CHAR_ADDITION.filter((char) => {
  return NAME.some((poke) => {
    return poke.slice(0, 2) === char;
  });
});

console.log("filteredFirstCharAddition :>> ", filteredFirstCharAddition);
