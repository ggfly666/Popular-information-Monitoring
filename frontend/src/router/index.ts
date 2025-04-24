import { createRouter, createWebHistory } from 'vue-router';
import { ElMessage } from 'element-plus';
import component from 'element-plus/es/components/tree-select/src/tree-select-option.mjs';

const routes = [
  { path: '/login', 
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/register', 
    component: () => import('@/views/Register.vue')
  },
  { path: '/', 
    redirect: '/sjdp',
    component: () => import('@/views/Home.vue'), 
    meta: { requiresAuth: true }, 
    children : [
      {
        path: '/sjdp',
        component: () => import('@/views/SJDP.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: '/hotlist',
        component: () => import('@/views/HotList.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: '/hotanalysis',
        component: () => import('@/views/HotAnalysis.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: '/push',
        component: () => import('@/views/Push.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: '/userinfo',
        component: () => import('@/views/UserInfo.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: '/crawlermanage',
        component: () => import('@/views/CrawlerManage.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: '/usermanage',
        component: () => import('@/views/UserManage.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'systemlog',
        component: () => import('@/views/SystemLog.vue'),
        meta: { requiresAuth: true }
      }
    ]
  },

];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  const username = localStorage.getItem('username');
  const isProtected = to.matched.some(record => record.meta.requiresAuth);
  if (isProtected && !username) {
    ElMessage.error('用户未登录，请先登录！');
    next('/login');
  } else {
    next();
  }
});

export default router;