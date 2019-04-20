import React from 'react';
import {shallow} from 'enzyme';
import renderer from 'react-test-renderer';
import Form from '../Form';
import {MemoryRouter as Router} from 'react-router-dom';

const testData = [
  {
    formType: 'Register',
    formData: {
      username: '',
      email: '',
      password: ''
    },
    handleUserFormSubmit: jest.fn(),
    handleFormChange: jest.fn(),
    isAuthenticated: false,
  }, {
    formType: 'Login',
    formData: {
      email: '',
      password: ''
    },
    handleUserFormSubmit: jest.fn(),
    handleFormChange: jest.fn(),
    isAuthenticated: false,
  }
]
describe('When not authenticated', () => {
  testData.forEach((ele) => {
    test(`${ele.formType} renders properly`, () => {
      const component = <Form isAuthenticated={false} formType={ele.formType} formData={ele.formData}/>;
      const wrapper = shallow(component);
      const h1 = wrapper.find('h1');
      expect(h1.length).toBe(1);
      expect(h1.get(0).props.children).toBe(ele.formType);
      const formGroup = wrapper.find('.form-group');
      expect(formGroup.length).toBe(Object.keys(ele.formData).length);
      expect(formGroup.get(0).props.children.props.name).toBe(Object.keys(ele.formData)[0]);
      expect(formGroup.get(0).props.children.props.value).toBe(ele.formData[Object.keys(ele.formData)[0]]);
    })
    test(`${ele.formType} Form renders a snapshot properly`, () => {
      const component = <Router location={`/${ele.formType}`}>
        <Form isAuthenticated={false} formType={ele.formType} formData={ele.formData}/>
      </Router>;
      const tree = renderer.create(component).toJSON();
      expect(tree).toMatchSnapshot();
    });
    const component = <Form {...ele} />;
    it(`${ele.formType} Form submits the form properly`, ()=>{
      const wrapper = shallow(component);
      const element = wrapper.find('input[name="email"]')
      expect(ele.handleFormChange).toHaveBeenCalledTimes(0);
      element.simulate('change');
      expect(ele.handleFormChange).toHaveBeenCalledTimes(1);
      expect(ele.handleUserFormSubmit).toHaveBeenCalledTimes(0);
      wrapper.find('form').simulate('submit',ele.formData)
      expect(ele.handleUserFormSubmit).toHaveBeenCalledWith(ele.formData);
      expect(ele.handleUserFormSubmit).toHaveBeenCalledTimes(1);
    })
  })
})
