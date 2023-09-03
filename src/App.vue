<script setup>
import { ref } from "vue";

// リアクティブな状態
const inputMsg = ref("");
const history = ref([]);
const loseMsgList = ref([]);
const errorMsgList = ref([]);

const submitMsg = () => {
  // エラーメッセージの初期化
  errorMsgList.value = [];

  // チェック処理
  if (validateMsg()) {
    // 敗北判定
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
    if (history.value.length > 0) {
      const lastWordLastChar = history.value.slice(-1)[0].substr(-1);
      const currentWordFirstChar = inputMsg.value[0];
      if (kanaToHira(lastWordLastChar) !== kanaToHira(currentWordFirstChar)) {
        loseMsgList.value.push(`前回の単語の末尾は 「${lastWordLastChar}」`);
      }
    }

    // 問題なければ履歴にpush
    history.value.push(inputMsg.value);
    // テキストボックスの初期化
    inputMsg.value = "";
  }
};

const retryGame = () => {
  history.value = [];
  loseMsgList.value = [];
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
</script>

<template>
  <h1>ポケしりとり</h1>
  <div>
    <template v-if="loseMsgList.length === 0">
      <h2>そこに　１つ　テキストボックスが　ある　じゃろう！</h2>
      <p v-if="history.length > 0">
        前回捕まえたポケモン: {{ history.slice(-1)[0] }}
      </p>
      <input
        type="text"
        v-model="inputMsg"
        required
        pattern="[\u30A1-\u30FC]*"
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
