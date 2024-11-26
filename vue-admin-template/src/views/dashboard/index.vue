<!-- <template>
  <div class="dashboard-container">
    <div class="dashboard-text">name: {{ name }}</div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Dashboard',
  computed: {
    ...mapGetters([
      'name'
    ])
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style> -->

<template>
  <div class="dashboard">
    <!-- 动态 SVG 背景 -->
    <div class="svg-background">
      <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
        <!-- 动态圆圈 -->
        <circle
          v-for="(circle, index) in circles"
          :key="index"
          :cx="circle.cx"
          :cy="circle.cy"
          :r="circle.r"
          :fill="circle.fill"
          :style="{ animationDelay: circle.delay }"
          class="circle"
        />
      </svg>
    </div>

    <!-- 欢迎文本 -->
    <h1 class="welcome-text">欢迎来到同济大学失物招领平台</h1>
  </div>
</template>

<script>
export default {
  name: "Dashboard",
  data() {
    return {
      circles: [
        { cx: "20%", cy: "50%", r: 40, fill: "rgba(255, 255, 255, 0.5)", delay: "0s" },
        { cx: "40%", cy: "30%", r: 60, fill: "rgba(255, 255, 255, 0.3)", delay: "1s" },
        { cx: "60%", cy: "70%", r: 50, fill: "rgba(255, 255, 255, 0.4)", delay: "2s" },
        { cx: "80%", cy: "40%", r: 70, fill: "rgba(255, 255, 255, 0.2)", delay: "3s" },
        { cx: "30%", cy: "80%", r: 50, fill: "rgba(255, 255, 255, 0.5)", delay: "4s" },
      ],
    };
  },
};
</script>

<style scoped>
/* 整体样式 */
.dashboard {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #e3f2fd, #90caf9);
  overflow: hidden;
  position: relative;
}

/* 欢迎文本样式 */
.welcome-text {
  position: relative;
  font-size: 48px;
  font-weight: bold;
  color: #ffffff;
  text-shadow: 4px 4px 8px rgba(0, 0, 0, 0.3);
  z-index: 1;
  animation: fadeIn 3s ease-in-out infinite;
}

/* SVG 背景样式 */
.svg-background {
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: 0;
}

.circle {
  animation: floatUp 5s infinite ease-in-out;
}

/* 动态圆圈上升动画 */
@keyframes floatUp {
  0% {
    transform: translateY(0);
    opacity: 0.6;
  }
  50% {
    transform: translateY(-20px);
    opacity: 1;
  }
  100% {
    transform: translateY(-40px);
    opacity: 0.6;
  }
}

/* 文本渐变动画 */
@keyframes fadeIn {
  0% {
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}
</style>



