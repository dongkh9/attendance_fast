<template>
    <div class="nav-container">
    <div class="title-container">
        <div class="logo-container">
        <img src="@/assets/img/yonsei.png" class="yonsei-logo" />
        </div>
        <p class="title">연세대학교 상남경영원 출석관리 시스템</p>
    </div>
    <div class="menu-container">
        <div class="menu-list">
        <RouterLink to="/attendance" class="menu-item" :class="{ 'menu-active': isAt }">
            출석관리
        </RouterLink>
        <RouterLink to="/course" class="menu-item" :class="{ 'menu-active': isCo }">
            교육과정
        </RouterLink>
        <RouterLink to="/excel" class="menu-item" :class="{ 'menu-active': isEx }">
            엑셀관리
        </RouterLink>
        <RouterLink to="/taglog" class="menu-item" :class="{ 'menu-active': isTa }">
            태그내역
        </RouterLink>
        </div>
    </div>
    </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

// 현재 경로에서 / 뒤 첫 단어 추출
const now_menu = computed(() => route.path.split('/')[1] || 'attendance')

// 각각의 탭 활성 상태를 computed로 관리
const isAt = computed(() => now_menu.value === 'attendance')
const isCo = computed(() => now_menu.value === 'course')
const isEx = computed(() => now_menu.value === 'excel')
const isTa = computed(() => now_menu.value === 'taglog')
console.log(isTa.value)
</script>

<style scoped>
.nav-container {
    padding: 0.2rem 0;
    border-bottom: solid black 4px;
    position: relative;
    top: 0;
}

.title-container {
    display: flex;
    align-items: center;
    margin-left: 30vw;
    cursor: default;
    user-select: none;
    
}

.title {
    font-size: 2vw;
    font-weight: 600;
    margin-left: 1rem;
}

.logo-container {
    width: 6vw;
    height: 6vw;
    padding: 0.3vw;
    display: flex;
    align-items: center;
    justify-content: center;
}

.yonsei-logo {
    width: 100%;
    height: 100%;
    object-fit: contain;
}

.menu-list {
    width: 60vw;
    display: flex;
    justify-content: space-between;
    margin-left: 20vw;
    margin-right: 20vw;
    margin-top: 0.1rem;
    
}

.menu-item {
    color: black;
    text-decoration: none;
    font-size: 1.5rem;
    font-weight: 500;
    padding: 0.5rem 1rem;
    transition: background-color 0.3s, color 0.3s;
    user-select: none;
    cursor: default;
}

.menu-item:hover,
.menu-active {
    color: royalblue;
    background-color: rgba(65, 105, 225, 0.3);
    border-radius: 10px;

}
</style>
