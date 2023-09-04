<script setup>
import { ref } from "vue";

// defineProps({
//   open: Boolean,
// });
const isOpen = ref(false);

const closeMenu = () => {
  isOpen.value = false;
};
</script>

<template>
  <div class="menu-wrapper" @click.self="closeMenu">
    <div class="menu-btn" @click="isOpen = !isOpen">
      <i class="fa fa-bars" aria-hidden="true"></i>
      <hr />
      <hr />
      <hr />
    </div>
    <div class="menu" v-bind:class="{ 'is-active': isOpen }">
      <div class="menu__item">TOP</div>
      <div class="menu__item">ABOUT</div>
      <div class="menu__item">BLOG</div>
      <div class="menu__item">CONTACT</div>
    </div>
  </div>
</template>

<style scoped>
.menu-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vw;
  z-index: 1;
}
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
</style>
