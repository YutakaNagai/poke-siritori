<script setup>
import { ref } from "vue";

const props = defineProps({
  config: Object,
});
const emit = defineEmits(["create-config"]);
const isOpenMenu = ref(false);

const closeMenu = () => {
  isOpenMenu.value = false;
};

const setConfig = (key, val) => {
  props.config[key] = val;
};

const updateConfig = () => {
  isOpenMenu.value = false;
  emit("create-config", props.config);
};
</script>

<template>
  <div class="menu-btn" @click="isOpenMenu = !isOpenMenu">
    <i class="fa fa-bars" aria-hidden="true"></i>
    <hr />
    <hr />
    <hr />
  </div>
  <div class="menu" v-bind:class="{ 'is-active': isOpenMenu }">
    <div class="menu__item">
      <h2>Config</h2>

      <div>
        <div class="title">最初の文字</div>
        <div v-if="props.config.randomFirstChar">
          <button
            class="switchBtn"
            @click="setConfig('randomFirstChar', !props.config.randomFirstChar)"
          >
            ランダム
          </button>
          <div class="explainText">
            <p>ゲーム開始時にランダムで文字が指定されます。</p>
          </div>
        </div>
        <div v-else>
          <button
            class="switchBtn"
            @click="setConfig('randomFirstChar', !props.config.randomFirstChar)"
          >
            指定なし
          </button>
          <div class="explainText">
            <p>ゲーム開始時は任意の文字から開始できます。</p>
          </div>
        </div>
      </div>

      <div>
        <div class="title">濁点/半濁点</div>
        <div v-if="props.config.ignoreMark">
          <button
            class="switchBtn"
            @click="setConfig('ignoreMark', !props.config.ignoreMark)"
          >
            同じ文字として扱う
          </button>
          <div class="explainText">
            <p>半濁点のついた文字とそうでない文字を同じ文字として扱います。</p>
            <p>ex) サンド → トドグラー ○</p>
          </div>
        </div>
        <div v-else>
          <button
            class="switchBtn"
            @click="setConfig('ignoreMark', !props.config.ignoreMark)"
          >
            違う文字として扱う
          </button>
          <div class="explainText">
            <p>
              濁点/半濁点のついた文字とそうでない文字を違う文字として扱います。
            </p>
            <p>ex) サンド → トドグラー ×</p>
          </div>
        </div>
      </div>

      <div>
        <div class="title">拗音</div>
        <div v-if="props.config.contractedTarget === 'secondlast'">
          <button
            class="switchBtn"
            @click="setConfig('contractedTarget', 'last')"
          >
            拗音の前の文字
          </button>
          <div class="explainText">
            <p>拗音の前の文字を次の開始文字として指定します。</p>
            <p>ガーディ → 「デ」からはじまる単語</p>
          </div>
        </div>
        <div v-else-if="props.config.contractedTarget === 'last'">
          <button
            class="switchBtn"
            @click="setConfig('contractedTarget', 'contracted')"
          >
            拗音
          </button>
          <div class="explainText">
            <p>大文字に変換後の拗音を次の開始文字として指定します。</p>
            <p>ガーディ → 「イ」からはじまる単語</p>
          </div>
        </div>
        <div v-else>
          <button
            class="switchBtn"
            @click="setConfig('contractedTarget', 'secondlast')"
          >
            拗音の前始まり
          </button>
          <div class="explainText">
            <p>拗音の前の文字以降を次の開始文字として指定します。</p>
            <p>ガーディ → 「ディ」からはじまる単語</p>
          </div>
        </div>
      </div>

      <div>
        <div class="title">末尾の長音</div>
        <div v-if="props.config.ignoreLastLong">
          <button
            class="switchBtn"
            @click="setConfig('ignoreLastLong', !props.config.ignoreLastLong)"
          >
            開始文字に含める
          </button>
          <div class="explainText">
            <p>
              末尾に長音がついていた場合、長音を含めた文字を次の開始文字とします。
            </p>
            <p>ex) エレブー → ブーバー</p>
          </div>
        </div>
        <div v-else>
          <button
            class="switchBtn"
            @click="setConfig('ignoreLastLong', !props.config.ignoreLastLong)"
          >
            開始文字に含めない
          </button>
          <div class="explainText">
            <p>
              末尾に長音がついていた場合、長音を含めない文字を次の開始文字とします。
            </p>
            <p>ex) エレブー → ブーバー</p>
          </div>
        </div>
      </div>
    </div>
    <div>
      <button @click="updateConfig">設定して新規ゲームを開始</button>
    </div>
  </div>
</template>

<style scoped>
/*----------------------------
* メニュー開閉ボタン
*----------------------------*/
.menu-btn {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 3;
  width: 40px;
  height: 40px;
  /* display: flex; */
  /* justify-content: center; */
  /* color: #fff; */
}

/*----------------------------
* メニュー本体
*----------------------------*/
.menu {
  position: fixed;
  top: 0;
  right: 0;
  z-index: 1;
  width: 60vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #555;
  opacity: 0.9;
}
.menu__item {
  width: 100%;
  height: auto;
  padding: 0.5em 1em;
  text-align: center;
  color: #fff;
  box-sizing: border-box;
}

/*----------------------------
* アニメーション部分
*----------------------------*/

/* アニメーション前のメニューの状態 */
.menu {
  transform: translateX(100vw);
  transition: all 0.5s linear;
}
/* アニメーション後のメニューの状態 */
.menu.is-active {
  transform: translateX(0);
}

.title {
  background: rgb(161, 158, 125);
}
.button-active {
  background: rgb(150, 218, 255);
}

.inline_block {
  display: inline-block;
}

.switchBtn {
  display: inline-block;
  width: 30%;
  top: 0;
  left: 0;
  margin-right: 10px;
  vertical-align: top;
}

.explainText {
  display: inline-block;
  width: 60%;
  top: 0;
  left: 0;
  font-size: small;
  text-align: left;
}
</style>
