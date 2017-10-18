import {combineReducers} from 'redux';

import homeReducer from './HomePage/reducer';

export function createReducer() {
  return combineReducers({
    home: homeReducer,
  })
}