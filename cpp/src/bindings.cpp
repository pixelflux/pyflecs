/* Copyright (c) 2022 Pixel Flux
 *
 * Permission is hereby granted, free of charge, to any person obtaining
 * a copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject to
 * the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
 * CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */


#include <iostream>

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

#include "world.hpp"
#include "entity.hpp"

namespace py = pybind11;
using namespace pyflecs;

void wrap_entity_set(entity* e, component *c, 
    py::array_t<uint8_t, py::array::c_style | py::array::forcecast> data)
{
    py::buffer_info info = data.request();
    e->set(*c, info.ptr);
}

py::array_t<uint8_t> wrap_entity_get(entity* e, component* c)
{
    auto ptr = reinterpret_cast<const uint8_t*>(e->get(*c));
    return py::array_t<uint8_t>(c->size(), ptr);
}

PYBIND11_MODULE(_flecs, m) {
    m.doc() = "Python bindings to flecs library";

    py::class_<entity>(m, "entity")
        .def("is_alive", &entity::is_alive)
        .def("destruct", &entity::destruct)
        .def("name", &entity::name)
        .def("add", &entity::add)
        .def("set", &wrap_entity_set)
        .def("get", &wrap_entity_get)
        .def("remove", &entity::remove)
        .def("raw", &entity::raw)
        ;

    py::class_<component>(m, "component")
        ;

    py::class_<world>(m, "world")
        .def(py::init<>())
        .def("entity", py::overload_cast<>(&world::entity))
        .def("entity", py::overload_cast<std::string>(&world::entity))
        .def("lookup", &world::lookup)
        .def("component", &world::component)
        ;

}