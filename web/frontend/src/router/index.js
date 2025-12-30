// src/router/index.js

import { createRouter, createWebHistory } from 'vue-router'
import ChatView from '../views/ChatView.vue'
import HeritageView from '../views/HeritageView.vue' 
import SpellCheckTest from '../views/SpellCheckTest.vue'

const routes = [
  { 
    path: '/chat', 
    name: 'Chat', 
    component: ChatView 
  },
  { 
    path: '/heritage',           
    name: 'Heritage',              
    component: HeritageView 
  },
  {
      path: '/test-spell',
      name: 'spell-test',
      component: SpellCheckTest
    }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router