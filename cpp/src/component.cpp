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

#include "component.hpp"

#include <stdexcept>

using namespace pyflecs;

component::component(ecs_world_t* world, std::string name, size_t size,
    size_t alignment) : 
        mpWorld(world),
        mSize(size)
{
    ecs_component_desc_t desc = { 0 }; 
        desc.entity.entity = 0; 
        desc.entity.name = name.c_str();
        desc.entity.symbol = name.c_str();
        desc.size = size;
        desc.alignment = alignment;
        mRaw = ecs_component_init(world, &desc);
        if (mRaw == 0)
            throw std::runtime_error("Component could not be created");
}

component::~component()
{

}