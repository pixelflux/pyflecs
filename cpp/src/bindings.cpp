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
#include <pybind11/stl.h>

#include "world.hpp"
#include "entity.hpp"
#include "filter.hpp"

namespace py = pybind11;
using namespace pyflecs;

void wrap_entity_set(entity* e, entity*c,
    py::array_t<uint8_t, py::array::c_style | py::array::forcecast> data)
{
    py::buffer_info info = data.request();
    e->set(*c, data.nbytes(), info.ptr);
}

py::array_t<uint8_t> wrap_entity_get(entity* e, entity* c)
{
    auto ptr = reinterpret_cast<const uint8_t*>(e->get(*c));
    // Must pass a dummy owner such that pybind will return the data without
    // modification: https://github.com/pybind/pybind11/issues/323
    py::str dummy;
    return py::array_t<uint8_t>(c->size(), ptr, dummy);
}

py::array_t<uint8_t> wrap_filter_iter_term(filter_iter *iter, entity& e, 
    int32_t idx)
{
    auto result = reinterpret_cast<const uint8_t*>(iter->term(e, idx));
    uint32_t size = iter->count() * e.size();
    py::str dummy; // See note above about ownership
    return py::array_t<uint8_t>(size, result, dummy);
}

PYBIND11_MODULE(_flecs, m) {
    m.doc() = "Python bindings to flecs library";

    py::class_<entity>(m, "entity")
        .def("is_alive", &entity::is_alive)
        .def("destruct", &entity::destruct)
        .def("name", &entity::name)
        .def("add", &entity::add)
        .def("set", &wrap_entity_set)
        .def("get", &wrap_entity_get, py::return_value_policy::reference)
        .def("remove", &entity::remove)
        .def("has", &entity::has)
        .def("raw", &entity::raw)

        // Pairs
        .def("add_pair", &entity::add_pair)
        .def("remove_pair", &entity::remove_pair)
        .def("has_pair", &entity::has_pair)

        // Hierarchies
        .def("path", &entity::path)
        .def("add_child", &entity::add_child)
        .def("lookup", &entity::lookup)
        
        // Instancing
        .def("is_a", &entity::is_a)

        // Type
        .def("type", &entity::type)
        ;

    py::class_<filter_iter>(m, "filter_iter")
        .def("next", &filter_iter::next)
        .def("term", &wrap_filter_iter_term, 
            py::return_value_policy::reference)
        ;

    py::class_<filter>(m, "filter")
        .def("iter", &filter::iter)
        ;

    py::class_<world>(m, "world")
        .def(py::init<>())
        .def("entity", py::overload_cast<>(&world::entity))
        .def("entity", py::overload_cast<std::string>(&world::entity))
        .def("lookup", &world::lookup)
        .def("lookup_path", &world::lookup_path)
        .def("component", &world::component)
        .def("create_filter", &world::create_filter)
        ;

}