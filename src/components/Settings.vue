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
        <div>
          <button
            @click="
              setConfig(
                'firstChar',
                props.config.firstChar === 'none' ? 'random' : 'none'
              )
            "
          >
            {{ props.config.firstChar === "none" ? "指定なし" : "ランダム" }}
          </button>
          <p>ゲーム開始時にランダムで文字が指定されます。</p>
        </div>
      </div>

      <div>
        <div class="title">濁点/半濁点</div>
        <div>
          <button @click="setConfig('ignoreMark', !props.config.ignoreMark)">
            {{
              props.config.ignoreMark
                ? "同じ文字として扱う"
                : "違う文字として扱う"
            }}
          </button>
          <p>
            {{
              props.config.ignoreMark
                ? "半濁点のついた文字とそうでない文字を同じ文字として扱います。"
                : "濁点/半濁点のついた文字とそうでない文字を違う文字として扱います。"
            }}
          </p>
          <p>
            {{
              props.config.ignoreMark
                ? "○ サンド → トドグラー"
                : "× サンド → トドグラー"
            }}
          </p>
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

.title {
  background: rgb(161, 158, 125);
}
.button-active {
  background: rgb(150, 218, 255);
}
</style>