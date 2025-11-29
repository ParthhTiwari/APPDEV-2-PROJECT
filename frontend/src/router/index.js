import { createRouter, createWebHistory } from 'vue-router';

import HomePage from '../pages/Home.vue';
import LoginPage from '../components/LoginForm.vue';
import RegisterPage from '../components/RegisterForm.vue';

import AdminDashboard from '../pages/AdminDashboard.vue';
import AdminCreateLot from '../pages/AdminCreateLot.vue';
import AdminLotsManagement from '../pages/AdminLotsManagement.vue';

import UserDashboard from '../pages/UserDashboard.vue';
import UserParkingHistory from '../pages/UserParkingHistory.vue';
import UserExportHistory from '../pages/UserExportHistory.vue';
import MonthlyReport from '../pages/MonthlyReport.vue';

const routes = [
  { path: '/', name: 'Home', component: HomePage },

  { path: '/login', name: 'Login', component: LoginPage },
  { path: '/register', name: 'Register', component: RegisterPage },

  // Admin Routes
  { path: '/admin/dashboard', name: 'AdminDashboard', component: AdminDashboard },
  { path: '/admin/create-lot', name: 'AdminCreateLot', component: AdminCreateLot },
  { path: '/admin/lots', name: 'AdminLotsManagement', component: AdminLotsManagement },

  // User Routes
  { path: '/user/dashboard', name: 'UserDashboard', component: UserDashboard },
  { path: '/user/history', name: 'UserParkingHistory', component: UserParkingHistory },
  { path: '/user/export', name: 'UserExportHistory', component: UserExportHistory },
  { path: '/user/monthly-report', name: 'MonthlyReport', component: MonthlyReport },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
