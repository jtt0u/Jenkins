// Простые тесты для приложения
console.log('Running tests...');

const tests = [];
let passed = 0;
let failed = 0;

// Тест 1: Проверка переменных окружения
function testEnvironmentVariables() {
  const requiredVars = ['NODE_ENV', 'APP_VERSION'];
  const missingVars = requiredVars.filter(varName => !process.env[varName]);

  if (missingVars.length === 0) {
    console.log('✓ Test 1: Environment variables check PASSED');
    return true;
  } else {
    console.log('✗ Test 1: Environment variables check FAILED - Missing:', missingVars.join(', '));
    return false;
  }
}

// Тест 2: Проверка версии приложения
function testAppVersion() {
  const version = process.env.APP_VERSION;

  if (version && version.match(/^\d+\.\d+\.\d+$/)) {
    console.log('✓ Test 2: Version format check PASSED');
    return true;
  } else {
    console.log('✗ Test 2: Version format check FAILED - Invalid version:', version);
    return false;
  }
}

// Тест 3: Проверка окружения
function testEnvironment() {
  const env = process.env.NODE_ENV;
  const validEnvironments = ['development', 'staging', 'production'];

  if (validEnvironments.includes(env)) {
    console.log('✓ Test 3: Environment validation PASSED');
    return true;
  } else {
    console.log('✗ Test 3: Environment validation FAILED - Invalid environment:', env);
    return false;
  }
}

// Тест 4: Проверка наличия зависимостей
function testDependencies() {
  try {
    require('express');
    console.log('✓ Test 4: Dependencies check PASSED');
    return true;
  } catch (error) {
    console.log('✗ Test 4: Dependencies check FAILED - Express not found');
    return false;
  }
}

// Запуск тестов
console.log('=================================');
console.log('Test Suite: Jenkins Sample App');
console.log('=================================\n');

tests.push(testEnvironmentVariables());
tests.push(testAppVersion());
tests.push(testEnvironment());
tests.push(testDependencies());

console.log('\n=================================');
tests.forEach(result => result ? passed++ : failed++);
console.log(`Total tests: ${tests.length}`);
console.log(`Passed: ${passed}`);
console.log(`Failed: ${failed}`);
console.log('=================================');

if (failed > 0) {
  console.log('\n❌ Tests FAILED\n');
  process.exit(1);
} else {
  console.log('\n✅ All tests PASSED\n');
  process.exit(0);
}
