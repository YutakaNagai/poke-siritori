<script setup>
import { onMounted, ref } from "vue";
import {
  NAME,
  FIRST_CHAR_ALLOW,
  DAKUTEN_CHAR_SET,
  DAKUTEN_HANDAKUTEN_CHAR_SET,
  FIRST_CHAR_ADDITION_ALLOW,
  YOUON_CHAR_SET,
} from "./util/const";
import Settings from "./components/Settings.vue";

// リアクティブな状態
const inputMsg = ref("");
const history = ref([]);
const loseMsgList = ref([]);
const winMsgList = ref([]);
const errorMsgList = ref([]);
const nextStartStr = ref("");
const config = ref({
  // ゲーム開始時の文字を指定するか true/false
  randomFirstChar: true,
  // 濁点/半濁点を同じ文字として認識するか false/true
  ignoreMark: true,
  // 末尾が拗音の場合、どの文字を開始文字とするか secondlast/last/contracted
  contractedTarget: "contracted",
  // 長音で終わっている場合長音の前の文字を開始文字とするか false/true
  ignoreLastLong: true,
});

const contractedList = [
  ...new Set(FIRST_CHAR_ADDITION_ALLOW.map((str) => str.slice(-1))),
];

const submitMsg = () => {
  // エラーメッセージの初期化
  errorMsgList.value = [];

  // チェック処理
  if (validateMsg()) {
    // 勝敗判定
    chkWord();

    inputMsg.value = hiraToKana(inputMsg.value);

    // 長音終わりの場合、設定によっては末尾の長音を削除 履歴登録時に改めて長音を復活
    let isDeleteLastLong = false;
    if (config.value.ignoreLastLong && inputMsg.value.endsWith("ー")) {
      inputMsg.value = inputMsg.value.slice(0, inputMsg.value.length - 1);
      isDeleteLastLong = true;
    }

    // 特殊単語時の判定
    // 後ろから２文字目
    const secondFromLastChar = inputMsg.value.slice(-2, -1);
    if (inputMsg.value.slice(-1) === "ー") {
      // 長音で終わっていた場合
      if (contractedList.includes(secondFromLastChar)) {
        // 後ろから2文字目が拗音だった場合
        if (config.value.contractedTarget === "secondlast") {
          // 後ろから3文字目を開始文字として設定
          nextStartStr.value = inputMsg.value.slice(-3, -2);
        } else if (config.value.contractedTarget === "last") {
          // 末尾の文字を大文字にして開始文字として設定
          nextStartStr.value = YOUON_CHAR_SET.find(
            (charset) => secondFromLastChar === charset[0]
          )[1];
        } else {
          // 後ろ3文字を開始文字として設定
          nextStartStr.value = inputMsg.value.slice(-3);
        }
      } else {
        nextStartStr.value = secondFromLastChar;
      }
    } else if (contractedList.includes(inputMsg.value.slice(-1))) {
      // 拗音で終わっていた場合
      if (config.value.contractedTarget === "secondlast") {
        // 後ろから2文字目を開始文字として設定
        nextStartStr.value = secondFromLastChar;
      } else if (config.value.contractedTarget === "last") {
        // 末尾の文字を大文字にして開始文字として設定
        nextStartStr.value = YOUON_CHAR_SET.find(
          (charset) => inputMsg.value.slice(-1) === charset[0]
        )[1];
      } else {
        // 後ろ2文字を開始文字として設定
        nextStartStr.value = inputMsg.value.slice(-2);
      }
    } else {
      nextStartStr.value = inputMsg.value.slice(-1);
    }
    console.log("nextStartStr.value :>> ", nextStartStr.value);

    // 返せる単語がなかったら勝利
    let candidate = null;
    // 濁点/半濁点を静音と同じ文字として扱う場合、charsetを要素として取得する
    const charSetList = [...nextStartStr.value].map((char) => {
      if (config.value.ignoreMark) {
        const dakutenCharSet = DAKUTEN_CHAR_SET.find((markCharSet) => {
          if (markCharSet.includes(char)) {
            return markCharSet;
          }
        });
        if (dakutenCharSet) {
          return dakutenCharSet;
        } else {
          return (
            DAKUTEN_HANDAKUTEN_CHAR_SET.find((markCharSet) => {
              if (markCharSet.includes(char)) {
                return markCharSet;
              }
            }) || [char]
          );
        }
      } else {
        return [char];
      }
    });
    const nextStartStrList = [];
    // 順列を網羅したリストを作成
    // 複雑になってしまうため、冗長だが1パターンずつ作成
    if (nextStartStr.value.length === 3) {
      // 3文字の場合
      for (let i = 0; i < charSetList[0].length; i++) {
        const permutation =
          charSetList[0][i] + charSetList[1][0] + charSetList[2][0];
        nextStartStrList.push(permutation);
      }
    } else if (nextStartStr.value.length === 2) {
      // 2文字の場合
      for (let i = 0; i < charSetList[0].length; i++) {
        const permutation = charSetList[0][i] + charSetList[1][0];
        nextStartStrList.push(permutation);
      }
    } else {
      // 1文字の場合
      for (let i = 0; i < charSetList[0].length; i++) {
        const permutation = charSetList[0][i];
        nextStartStrList.push(permutation);
      }
    }

    if (history.value.length > 0) {
      candidate = NAME.find(
        (word) =>
          !history.value.includes(word) &&
          !word.endsWith("ン") &&
          nextStartStrList.find((str) => word.startsWith(str))
      );
    } else {
      candidate = NAME.find(
        (word) =>
          !word.endsWith("ン") &&
          nextStartStrList.find((str) => word.startsWith(str))
      );
    }
    if (!candidate) {
      winMsgList.value.push(`「${nextStartStr.value}」 で返せる単語がない`);
    }

    // 末尾の長音を削除していた場合、ここで復活
    if (isDeleteLastLong) {
      inputMsg.value = inputMsg.value + "ー";
    }

    // 履歴にpush
    history.value.push(inputMsg.value);

    // テキストボックスの初期化
    inputMsg.value = "";
  }
};

const retryGame = () => {
  history.value = [];
  loseMsgList.value = [];
  winMsgList.value = [];
  if (config.value.randomFirstChar) {
    nextStartStr.value =
      FIRST_CHAR_ALLOW[Math.floor(Math.random() * FIRST_CHAR_ALLOW.length)];
  } else {
    nextStartStr.value = "";
  }
};

const hiraToKana = (str) => {
  return str.replace(/[\u3041-\u3096]/g, function (match) {
    var chr = match.charCodeAt(0) + 0x60;
    return String.fromCharCode(chr);
  });
};

const kanaToHira = (str) => {
  return str.replace(/[\u30a1-\u30f6]/g, function (match) {
    var chr = match.charCodeAt(0) - 0x60;
    return String.fromCharCode(chr);
  });
};

const validateMsg = () => {
  if (!inputMsg.value) {
    errorMsgList.value.push("ワードを入力してください");
    return false;
  } else if (!inputMsg.value.match(/^[ぁ-んァ-ヶー]*$/)) {
    errorMsgList.value.push(
      "全角のひらがな・カタカナ・長音記号のみ入力可能です"
    );
    return false;
  } else {
    return true;
  }
};

const chkWord = () => {
  // 「ん」で終わっていたら敗北
  const lastChar = inputMsg.value.slice(-1);
  if (lastChar === "ん" || lastChar === "ン") {
    loseMsgList.value.push(`「${lastChar}」 で終わってしまった`);
  }

  // 同じ単語が出てきたら敗北
  if (history.value.includes(inputMsg.value)) {
    loseMsgList.value.push(`「${inputMsg.value}」 は既に使用済み`);
  }

  const KanaPrevLast = hiraToKana(nextStartStr.value);
  let KanaCurrentFirst = "";
  if (config.value.contractedTarget === "contracted") {
    KanaCurrentFirst = hiraToKana(inputMsg.value.slice(0, KanaPrevLast.length));
  } else {
    KanaCurrentFirst = hiraToKana(inputMsg.value.slice(0, 1));
  }

  // 各判定で敗北したかどうか判別するためのフラグ
  let isMarkSafe = false;

  // 前の単語と繋がっているか判定
  if (!!nextStartStr.value) {
    // configごとの設定
    if (config.value.ignoreMark) {
      // 濁点
      for (const charset of DAKUTEN_CHAR_SET) {
        if (KanaPrevLast === charset[0] || KanaPrevLast === charset[1]) {
          if (
            KanaCurrentFirst === charset[0] ||
            KanaCurrentFirst === charset[1]
          ) {
            isMarkSafe = true;
            break;
          } else if (KanaPrevLast !== KanaCurrentFirst) {
            // 前の単語と繋がっていなかったら敗北
            loseMsgList.value.push(
              `前回の単語の末尾は 「${nextStartStr.value}」`
            );
          }
        }
      }
      if (!isMarkSafe) {
        // 濁点/半濁点
        for (const charset of DAKUTEN_HANDAKUTEN_CHAR_SET) {
          if (
            KanaPrevLast === charset[0] ||
            KanaPrevLast === charset[1] ||
            KanaPrevLast === charset[2]
          ) {
            if (
              KanaCurrentFirst === charset[0] ||
              KanaCurrentFirst === charset[1] ||
              KanaCurrentFirst === charset[2]
            ) {
              isMarkSafe = true;
              break;
            } else if (KanaPrevLast !== KanaCurrentFirst) {
              // 前の単語と繋がっていなかったら敗北
              loseMsgList.value.push(
                `前回の単語の末尾は 「${nextStartStr.value}」`
              );
            }
          }
        }
      }
      if (!isMarkSafe && KanaPrevLast !== KanaCurrentFirst) {
        // 前の単語と繋がっていなかったら敗北
        loseMsgList.value.push(`前回の単語の末尾は 「${nextStartStr.value}」`);
      }
    } else if (KanaPrevLast !== KanaCurrentFirst) {
      // 前の単語と繋がっていなかったら敗北
      loseMsgList.value.push(`前回の単語の末尾は 「${nextStartStr.value}」`);
    }
  }

  // 存在しないポケモンの場合敗北
  if (!NAME.includes(hiraToKana(inputMsg.value))) {
    loseMsgList.value.push(`「${inputMsg.value}」 は存在しないポケモンです`);
  }
};

const surrender = () => {
  // エラーメッセージの初期化
  errorMsgList.value = [];
  // テキストボックスの初期化
  inputMsg.value = "";

  loseMsgList.value.push("降参しました");
};

const createConfig = (newConfig) => {
  config.value = newConfig;
  retryGame();
};

// onMounted(() => {
//   // 開始文字の初期化（ランダム取得）
//   nextStartStr.value =
//     FIRST_CHAR_ALLOW[Math.floor(Math.random() * FIRST_CHAR_ALLOW.length)];
// });
</script>

<template>
  <Settings :config="config" @create-config="createConfig" />
  <h1>ポケしりとり</h1>
  <div>
    <template v-if="loseMsgList.length === 0 && winMsgList.length === 0">
      <h2>そこに　１つ　テキストボックスが　ある　じゃろう！</h2>
      <div v-if="!!nextStartStr">最初の文字: {{ nextStartStr }}</div>
      <template v-if="history.length > 0 && loseMsgList.length === 0">
        <p>前回捕まえたポケモン: {{ history.slice(-1)[0] }}</p>
        <button @click="surrender">にげる</button>
      </template>

      <input
        type="text"
        v-model="inputMsg"
        required
        pattern="[\u30A1-\u30FC]*"
        @keypress.enter="submitMsg"
      />
      <button @click="submitMsg">送信</button>

      <p v-for="(msg, index) in errorMsgList" :key="index" class="error_msg">
        {{ msg }}
      </p>
    </template>

    <!-- 敗北時処理 -->
    <div v-if="loseMsgList.length !== 0">
      <h2>めのまえが　まっくらに　なった！</h2>
      <template v-for="(loseMsg, index) in loseMsgList" :key="index">
        <h3>敗因{{ index + 1 }}: {{ loseMsg }}</h3>
      </template>
      <button @click="retryGame">リトライ</button>
    </div>

    <!-- 勝利時処理 -->
    <div v-else-if="winMsgList.length !== 0">
      <h2>こうかは　ばつぐんだ！</h2>
      <template v-for="(winMsg, index) in winMsgList" :key="index">
        <h3>勝因{{ index + 1 }}: {{ winMsg }}</h3>
      </template>
      <button @click="retryGame">リトライ</button>
    </div>

    <!-- 履歴 -->
    <h2 v-if="history.length > 0">捕まえたポケモン</h2>
    <div v-for="(msg, index) in history" :key="index">
      <span v-if="index > 0">→ </span>{{ msg }}
    </div>
  </div>
</template>

<style scoped>
input {
  font-size: 16px;
}

.error_msg {
  color: red;
}
</style>
