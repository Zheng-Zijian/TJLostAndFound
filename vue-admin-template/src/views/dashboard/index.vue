
<template>
  <div class="home-page">

    <!-- 顶部导航栏 -->
    <header class="header">
      <div class="header-content">
        <div class="logo">
          <img src="@/assets/tongji_logo.jpg" alt="同济大学" height="40" />
          <span class="platform-name">同济大学失物招领平台</span>
        </div>
      </div>
      <hr class="header-divider" />
    </header>

    <!-- 走马灯展示区 -->
    <section class="carousel-section">
      <el-carousel indicator-position="outside" height="600px" arrow="always">
        <el-carousel-item v-for="(img, index) in carouselImages" :key="index">
          <div class="carousel-item-content" :style="{ backgroundImage: 'url(' + img.url + ')' }">
            <!-- 半透明遮罩层与文本 -->
            <div class="carousel-overlay">
              <h2 class="welcome-text">欢迎来到同济大学失物招领平台</h2>
              <p class="intro-text">帮助同学们快速查找遗失物品并及时认领，营造更有序的校园环境。</p>
            </div>
          </div>
        </el-carousel-item>
      </el-carousel>
    </section>

  
    <!-- 平台简介 -->
    <section class="platform-intro-section">
      <el-row type="flex" align="middle" justify="center" :gutter="20">
        <el-col :sm="24" :md="10">
          <h2>平台简介</h2>
          <p>同济大学失物招领平台由校方与学生组织共同搭建。  
             在这里，你可以轻松查找校园中登记过的失物信息，也可以及时发布自己遗失的物品公告。  
             我们希望通过这个平台，进一步加强校园内的互助与信任，让失物与物主能够更快、更便利地相遇。
          </p>
        </el-col>
        <el-col :sm="24" :md="8">
          <img src="@/assets/campus/campus4.png" alt="校园景观" class="intro-img" />
        </el-col>
      </el-row>
    </section>

    <!-- 页脚 -->
    <footer class="footer">
      <div class="footer-content">
        <p>© 2024 同济大学 | 联系方式：xxx@tongji.edu.cn</p>
      </div>
    </footer>

  </div>
</template>

<script>
export default {
  name: 'HomePage',
  data() {
    return {
      carouselImages: [
        { url: require('@/assets/campus/campus1.jpeg') },
        { url: require('@/assets/campus/campus2.jpeg') },
        { url: require('@/assets/campus/campus3.jpeg') },
      ]
    }
  }
}
</script>

<style scoped>
.home-page {
  font-family: 'Helvetica', 'Arial', sans-serif;
  color: #333;
  background-color: #fff;
}

/* 顶部导航 */
.header {
  padding: 0 20px;
  background: #fff;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
}

.logo {
  display: flex;
  align-items: center;
}

.logo img {
  margin-right: 10px;
}

.platform-name {
  font-weight: bold;
  font-size: 16px;
}

.nav {
  display: flex;
  gap: 20px;
}

.header-divider {
  border: none;
  border-bottom: 1px solid #eaeaea;
}

/* 走马灯区 */
.carousel-section {
  position: relative;
}

.carousel-item-content {
  background-size: cover;
  background-position: center;
  height: 600px;
  position: relative;
}

.carousel-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 40px;
  background: linear-gradient(to top, rgba(0,0,0,0.4), transparent);
  color: #fff;
}

.welcome-text {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
}

.intro-text {
  font-size: 16px;
}


/* 平台简介区 */
.platform-intro-section {
  padding: 60px 20px;
}

.platform-intro-section h2 {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

.platform-intro-section p {
  line-height: 1.6;
  font-size: 14px;
}

.intro-img {
  width: 100%;
  border-radius: 8px;
}

/* 底部 */
.footer {
  border-top: 1px solid #eaeaea;
  padding: 20px;
  text-align: center;
  font-size: 12px;
  color: #666;
}
</style>
