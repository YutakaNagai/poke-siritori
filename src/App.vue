<script setup>
import { onMounted, ref } from "vue";
import { NAME, FIRST_CHAR_ALLOW } from "./util/const";
import Settings from "./components/Settings.vue";

// リアクティブな状態
const inputMsg = ref("");
const history = ref([]);
const loseMsgList = ref([]);
const errorMsgList = ref([]);
const nextStartStr = ref("");
const config = ref({
  firstChar: "none",
});

const submitMsg = () => {
  // エラーメッセージの初期化
  errorMsgList.value = [];

  // チェック処理
  if (validateMsg()) {
    // 敗北判定
    chkLose();

    // 特殊単語時の判定
    // 長音で終わっていた場合
    if (inputMsg.value.slice(-1) === "ー") {
      nextStartStr.value = inputMsg.value.slice(-2, -1);
    } else {
      nextStartStr.value = inputMsg.value.slice(-1);
    }
    // TODO: 小文字、複数文字、それらの設定

    // 履歴にpush
    history.value.push(inputMsg.value);

    // テキストボックスの初期化
    inputMsg.value = "";
  }
};

const retryGame = () => {
  history.value = [];
  loseMsgList.value = [];
  if (config.value.firstChar === "random") {
    nextStartStr.value =
      FIRST_CHAR_ALLOW[Math.floor(Math.random() * FIRST_CHAR_ALLOW.length)];
  } else {
    nextStartStr.value = "";
  }
};

const kanaToHira = (str) => {
  return str.replace(/[\u30a1-\u30f6]/g, (match) => {
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

const chkLose = () => {
  // 「ん」で終わっていたら敗北
  const lastChar = inputMsg.value.slice(-1);
  if (lastChar === "ん" || lastChar === "ン") {
    loseMsgList.value.push(`「${lastChar}」 で終わってしまった`);
  }

  // 同じ単語が出てきたら敗北
  if (history.value.includes(inputMsg.value)) {
    loseMsgList.value.push(`「${inputMsg.value}」 は既に使用済み`);
  }

  // 前の単語と繋がっていなかったら敗北
  if (!!nextStartStr.value) {
    const currentWordFirstChar = inputMsg.value[0];
    if (kanaToHira(nextStartStr.value) !== kanaToHira(currentWordFirstChar)) {
      loseMsgList.value.push(`前回の単語の末尾は 「${nextStartStr.value}」`);
    }
  }

  // 存在しないポケモンの場合敗北
  if (!NAME.includes(inputMsg.value)) {
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
    <template v-if="loseMsgList.length === 0">
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
