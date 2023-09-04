<script setup>
import { ref } from "vue";

const props = defineProps({
  config: Object,
});
const emit = defineEmits(["create-config"]);
const isOpen = ref(false);

const closeMenu = () => {
  isOpen.value = false;
};

const setConfig = (key, val) => {
  props.config[key] = val;
};

const updateConfig = () => {
  isOpen.value = false;
  emit("create-config", props.config);
};
</script>

<template>
  <div class="menu-btn" @click="isOpen = !isOpen">
    <i class="fa fa-bars" aria-hidden="true"></i>
    <hr />
    <hr />
    <hr />
  </div>
  <div class="menu" v-bind:class="{ 'is-active': isOpen }">
    <div class="menu__item">
      <h2>Config</h2>
      <div>
        <p>最初の文字</p>
        <div>
          <button
            :class="{ 'button-active': props.config.firstChar === 'none' }"
            @click="setConfig('firstChar', 'none')"
          >
            指定なし
          </button>
          <button
            :class="{ 'button-active': props.config.firstChar === 'random' }"
            @click="setConfig('firstChar', 'random')"
          >
            ランダム
          </button>
        </div>
      </div>
    </div>
    <button @click="updateConfig">設定して新規ゲームを開始</button>
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

.button-active {
  background: rgb(150, 218, 255);
}
</style>
