from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class SeleniumHelper:
	driver = None
	WAIT = 99999

	def loadPage(self, page):
		try:
			self.driver.get(page)
			return True
		except:
			return False

	def submitForm(self, element):
		try:
			element.submit()
			return True
		except TimeoutException:
			return False

	def waitShowElement(self, selector, wait=99999):
		try:
			wait = WebDriverWait(self.driver, wait)
			element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
			return element
		except:
			return None

	def waitHideElement(self, selector, wait):
		try:
			wait = WebDriverWait(self.driver, wait)
			element = wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, selector)))
			return element
		except:
			return None

	def getElementFrom(self, fromObject, selector):
		try:
			return fromObject.find_element_by_css_selector(selector)
		except NoSuchElementException:
			return None

	def getElementsFrom(self, fromObject, selector):
		try:
			return fromObject.find_elements_by_css_selector(selector)
		except NoSuchElementException:
			return None		

	def getElement(self, selector):
		return self.getElementFrom(self.driver, selector)

	def getElements(self, selector):
		return self.getElementsFrom(self.driver, selector)

	def getElementFromValue(self, fromObject, selector):
		element = self.getElementFrom(fromObject, selector)
		if element:
			return element.text
		return None

	def getElementValue(self, selector):
		element = self.getElement(selector)
		if element:
			return element.text
		return None

	def getElementFromAttribute(self, fromObject, selector, attribute):
		element = self.getElementFrom(fromObject, selector)
		if element:
			return element.get_attribute(attribute)
		return None

	def getElementAttribute(self, selector, attribute):
		element = self.getElement(selector)
		if element:
			return element.get_attribute(attribute)
		return None

	def getParentLevels(self, node, levels):
		path = '..'
		if levels > 1:
			for i in range(1, levels):
				path = path + '/..'
		return node.find_element_by_xpath(path)

	def getParentNode(self, node):
		return node.find_element_by_xpath('..')

	def getChildNodes(self, node):
		return node.find_elements_by_xpath('./*')

	def selectAndWrite(self, field, value):
		fieldObject = self.getElement(field)
		fieldObject.send_keys(value)
		return fieldObject

	def waitAndWrite(self, field, value):
		fieldObject = self.waitShowElement(field, self.WAIT)
		fieldObject.send_keys(value)
		return fieldObject

	def pressEnter(self, fieldObject):
		fieldObject.send_keys(Keys.RETURN)
		return fieldObject

	def click(self, element):
		actions = webdriver.ActionChains(self.driver)
		actions.move_to_element(element)
		actions.click(element)
		actions.perform()

	def moveToElement(self, element):
		self.driver.execute_script("return arguments[0].scrollIntoView();", element)
		actions = webdriver.ActionChains(self.driver)
		actions.move_to_element(element)
		actions.perform()

	def saveScreenshot(self, path="screenshot.png"):
		self.driver.save_screenshot(path) 