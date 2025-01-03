import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  {
    path: '/register',
    component: () => import('@/views/register/index'),
    hidden: true
  },
  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: '主页面',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '主页面', icon: 'dashboard' }
    }]
  },
  {
    path: '/table',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'Form',
        component: () => import('@/views/table/index'),
        meta: { title: '失物表', icon: 'table' }
      }
    ]
  },

  {
    path: '/personal',
    component: Layout,
    meta: { title: '个人中心', icon: 'user' }, // 新增：外层添加icon
    children: [
      {
        path: 'upload',
        name: '上传失物列表',
        component: () => import('@/views/personal/upload'),
        meta: { title: '上传失物列表', icon: 'table' }
      },
      {
        path: 'requests',
        name: '认领请求列表',
        component: () => import('@/views/personal/requests'),
        meta: { title: '认领请求列表', icon: 'el-icon-bell' }
      }
    ]
  },
  {
    path: '/info',
    component: Layout,
    meta: { title: '信息管理', icon: 'el-icon-s-order' ,roles: ['admin'] },
    children: [
      {
        path: 'manage',
        name: 'InfoManage',
        component: () => import('@/views/info/InfoManage'),
        meta: { title: '发布信息', icon: 'el-icon-s-order' }
      },
      {
        path: 'list',
        name: 'InfoList',
        component: () => import('@/views/info/InfoList'),
        meta: { title: '信息列表', icon: 'el-icon-s-order' } // 所有人可访问
      }
    ]
  }
  // 404 page must be placed at the end !!!
  // { path: '*', redirect: '/404', hidden: true }
]

export const asyncRoutes = [
  {
    path: '/admin',
    component: Layout,
    meta: { title: '管理员权限', icon: 'el-icon-s-order',roles: ['admin'] },
    children: [
      {
        path: 'admin',
        name: 'adminList',
        // redirect: '/admin/admin',
        component: () => import('@/views/admin/index'),
        meta: { title: '管理员权限', roles: ['admin'] } // 所有人可访问
      }
    ]
  },
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  mode: 'hash', // 改为 hash 模式，避免刷新问题
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter() // 在 createRouter 定义之后调用

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // 重置路由
}

export default router
